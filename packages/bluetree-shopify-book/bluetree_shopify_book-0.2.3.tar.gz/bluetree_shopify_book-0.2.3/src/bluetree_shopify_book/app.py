from __future__ import annotations

import json
import typing as t
from decimal import Decimal
from pathlib import Path

import shopify

from .adapters import to_metafield_definition, to_shopify_book, to_shopify_shop
from .schema import (
    CreateBookInput,
    CreateMetafieldDefinitionInput,
    MetafieldDefinition,
    MetafieldType,
    Publication,
    ShopifyBook,
)
from .utils import concunrrently_handle_tasks

document = (Path(__file__).resolve().parent / "document.graphql").read_text()


class ShopifyBookService:
    """
    A service for managing books in a Shopify store.

    Args:
        shop_url (str): The URL of the Shopify store.
        admin_api_access_token (str): The Shopify API access token for the store.
        api_version (str, optional): The version of the Shopify API to use. Defaults to "2023-01".
    """

    def __init__(
        self,
        shop_url: str,
        admin_api_access_token: str,
        api_version: str = "2023-01",
    ) -> None:
        self._session = shopify.Session(shop_url, api_version, admin_api_access_token)

    def __enter__(self) -> ShopifyBookService:
        """
        Enables the Shopify API session when entering a context.
        """
        shopify.ShopifyResource.activate_session(self._session)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Clears the Shopify API session when exiting a context.
        """
        shopify.ShopifyResource.clear_session()

    def get_shop(self) -> dict:
        """
        Gets information about the Shopify store.

        Returns:
            dict: A dictionary containing information about the store.
        """
        result = shopify.GraphQL().execute("{ shop { name id, myshopifyDomain } }")
        data = json.loads(result)
        shop = to_shopify_shop(data["data"]["shop"])
        return shop

    def get_book_by_id(self, product_id: int) -> t.Optional[ShopifyBook]:
        """
        Gets a book by its product ID.

        Args:
            product_id (int): The ID of the book's product.

        Returns:
            Optional[ShopifyBook]: A ShopifyBook object representing the book, or None if no book was found with the
            specified ID.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(id=f"gid://shopify/Product/{product_id}"),
            operation_name="product",
        )
        data = json.loads(result)
        return to_shopify_book(data["data"]["product"])

    def get_book_by_isbn(self, isbn: str) -> t.Optional[ShopifyBook]:
        """
        Gets a book by its ISBN.

        Args:
            isbn (str): The ISBN of the book.

        Returns:
            Optional[ShopifyBook]: A ShopifyBook object representing the book, or None if no book was found with the
            specified ISBN.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(filter=f"sku:{isbn}"),
            operation_name="productByISBN",
        )
        data = json.loads(result)
        edges = data["data"]["productVariants"]["edges"]
        if len(edges) == 0:
            return None
        return to_shopify_book(edges[0]["node"]["product"])
    
    def check_has_book(self, isbn: str) -> bool:
        """
        Checks if a book with the given ISBN exists in the Shopify store.

        Args:
            isbn (str): The ISBN of the book to check.

        Returns:
            bool: True if a book with the given ISBN exists in the Shopify store, False otherwise.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(filter=f"sku:{isbn}"),
            operation_name="productVariantByISBN",
        )
        data = json.loads(result)
        has_book = len(data["data"]["productVariants"]["edges"]) > 0
        return has_book

    def create_book(self, book_input: CreateBookInput) -> ShopifyBook:
        """
        Creates a new book in the Shopify store.

        Args:
            book_input (CreateBookInput): A CreateBookInput object representing the new book.

        Returns:
            ShopifyBook: A ShopifyBook object representing the new book.
        """
        try:
            result = shopify.GraphQL().execute(
                query=document,
                variables=dict(input=book_input.to_input_data()),
                operation_name="productCreate",
            )
            data = json.loads(result)
            return to_shopify_book(data["data"]["productCreate"]["product"])
        except KeyError:
            raise ValueError(data["errors"])

    def create_books(self, book_inputs: t.List[CreateBookInput]) -> t.List[ShopifyBook]:
        """
        Creates multiple books concurrently in the Shopify store.

        Args:
            book_inputs (List[CreateBookInput]): A list of CreateBookInput objects representing the new books.

        Returns:
            List[ShopifyBook]: A list of ShopifyBook objects representing the new books.
        """
        results = concunrrently_handle_tasks(
            [lambda: self.create_book(book_input) for book_input in book_inputs]
        )
        return [result.get_result() for result in results]

    def update_book_price(self, product_variant_id: int, price: Decimal) -> ShopifyBook:
        """
        Updates the price of a book in the Shopify store.

        Args:
            product_variant_id (int): The ID of the book's product variant.
            price (Decimal): The new price of the book.

        Returns:
            ShopifyBook: A ShopifyBook object representing the updated book.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(
                input=dict(
                    id=f"gid://shopify/ProductVariant/{product_variant_id}",
                    price=str(price),
                )
            ),
            operation_name="productVariantUpdate",
        )
        data = json.loads(result)
        return data

    def delete_book(self, product_id: int):
        """
        Deletes a book from the Shopify store.

        Args:
            product_id (int): The ID of the book's product.
        """
        shopify.GraphQL().execute(
            query=document,
            variables=dict(input={"id": f"gid://shopify/Product/{product_id}"}),
            operation_name="productDelete",
        )

    def add_products_to_collection(self, collection_id: int, product_ids: list[int]):
        """
        Add one or more products to a Shopify collection.

        Args:
            collection_id (int): The ID of the collection to add products to.
            product_ids (list[int]): A list of product IDs to add to the collection.

        Returns:
            dict: A dictionary representing the response data from the Shopify API.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(
                id=f"gid://shopify/Collection/{collection_id}",
                productIds=[
                    f"gid://shopify/Product/{product_id}" for product_id in product_ids
                ],
            ),
            operation_name="collectionAddProductsV2",
        )
        data = json.loads(result)
        return data

    def get_publications(self) -> list[Publication]:
        """
        Gets a list of publications in the Shopify store.

        Returns:
            list[any]: A list of publication objects.
        """
        result = shopify.GraphQL().execute(
            query=document, operation_name="publications"
        )
        data = json.loads(result)
        publications: t.List[Publication] = []
        for edge in data["data"]["publications"]["edges"]:
            pub_data = edge["node"]
            publications.append(Publication(gid=pub_data["id"], name=pub_data["name"]))
        return publications

    def publish_product(self, product_id: int, publication_ids: list[int]) -> dict:
        """
        Publishes a product to one or more publications.

        Args:
            product_id (int): The ID of the product to be published.
            publication_ids (list[int]): A list of publication IDs to which the product will be published.

        Returns:
            dict: A dictionary containing the result of the GraphQL query executed to publish the product.

        Raises:
            Any exceptions that may be raised by the Shopify GraphQL API.

        Example usage:
            publish_product(12345, [67890, 12345])
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(
                id=f"gid://shopify/Product/{product_id}",
                input=[
                    {"publicationId": f"gid://shopify/Publication/{publication_id}"}
                    for publication_id in publication_ids
                ],
            ),
            operation_name="publishablePublish",
        )
        return result

    def setup_default_metafield_definitions(self):
        """
        Sets up default metafield definitions for books in the Shopify store.
        """
        self._create_metafield_definition(
            CreateMetafieldDefinitionInput(
                name="Author",
                key="author",
                type=MetafieldType.single_line_text_field,
            )
        )
        self._create_metafield_definition(
            CreateMetafieldDefinitionInput(
                name="Published Date",
                key="published_date",
                type=MetafieldType.single_line_text_field,
            )
        )
        self._create_metafield_definition(
            CreateMetafieldDefinitionInput(
                name="ISBN",
                key="isbn",
                type=MetafieldType.single_line_text_field,
            )
        )
        self._create_metafield_definition(
            CreateMetafieldDefinitionInput(
                name="Staff Comment",
                key="staff_comment",
                type=MetafieldType.single_line_text_field,
            )
        )
        self._create_metafield_definition(
            CreateMetafieldDefinitionInput(
                name="Backorder",
                key="backorder",
                type=MetafieldType.boolean,
            )
        )

    def _get_metafield_definitions(self) -> t.List[MetafieldDefinition]:
        """
        Gets all metafield definitions in the Shopify store.

        Returns:
            List[MetafieldDefinition]: A list of MetafieldDefinition objects representing the metafield definitions in
            the Shopify store.
        """
        result = shopify.GraphQL().execute(
            query=document,
            operation_name="metafieldDefinitions",
        )
        data = json.loads(result)
        metafield_definitions = [
            to_metafield_definition(edge["node"])
            for edge in data["data"]["metafieldDefinitions"]["edges"]
        ]
        return metafield_definitions

    def _create_metafield_definition(
        self, metafield_definition_input: CreateMetafieldDefinitionInput
    ) -> bool:
        """
        Creates a new metafield definition in the Shopify store.

        Args:
            metafield_definition_input (CreateMetafieldDefinitionInput): A CreateMetafieldDefinitionInput object
            representing the new metafield definition.

        Returns:
            MetafieldDefinition: A MetafieldDefinition object representing the new metafield definition.
        """
        result = shopify.GraphQL().execute(
            query=document,
            variables=dict(definition=metafield_definition_input.to_input_data()),
            operation_name="metafieldDefinitionCreate",
        )
        data = json.loads(result)
        return "errors" not in data
