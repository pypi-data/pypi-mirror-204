from __future__ import annotations

import abc
import typing as t
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, validator

from bluetree_shopify_book.utils import sanitize_description

from .validators import is_valid_isbn, is_valid_url, sanitize_isbn


class QuerySchema(BaseModel):
    gid: str

    @property
    def id(self) -> int:
        return int(self.gid.split("/")[-1])


class MutationSchema(BaseModel, abc.ABC):
    @abc.abstractmethod
    def to_input_data(self) -> dict:
        raise NotImplementedError


class ShopifyShop(QuerySchema):
    name: str
    myshopify_domain: str


class ShopifyBook(QuerySchema):
    isbn: str
    title: str
    author: t.Optional[str]
    price: t.Optional[Decimal]
    subtitle: t.Optional[str]
    description: t.Optional[str]
    publisher: t.Optional[str]
    published_date: t.Optional[str]


class CreateBookInput(MutationSchema):
    isbn: str
    title: str
    author: str
    price: Decimal
    is_backorder: bool = True
    location_ids: list[t.Union[int, list[int, int]]] = []
    collection_ids: list[int] = []
    product_type: str = "Textbook"
    subtitle: t.Optional[str] = None
    description: t.Optional[str] = None
    publisher: t.Optional[str] = None
    published_date: t.Optional[str] = None
    cover_image: t.Optional[str] = None
    staff_comment: t.Optional[str] = None
    tags: list[str] = []

    @validator("isbn")
    def isbn_must_be_10_or_13_digits(cls, v):
        if not is_valid_isbn(v):
            raise ValueError("ISBN must be 10 or 13 digits")
        return sanitize_isbn(v)

    @validator("description")
    def description_must_be_html(cls, v):
        return sanitize_description(v)

    @validator("cover_image")
    def cover_image_must_be_url(cls, v):
        if v is None:
            return v
        if not is_valid_url(v):
            raise ValueError("Cover image must be a URL")
        return v

    def to_input_data(self) -> dict:
        data = {
            "title": self.title,
            "vendor": self.publisher,
            "descriptionHtml": self.description,
            "productType": self.product_type,
            "tags": self.tags,
            "variants": [
                {
                    "sku": self.isbn,
                    "barcode": self.isbn,
                    "price": str(self.price),
                    "inventoryItem": {
                        "tracked": True,
                    },
                }
            ],
            "productCategory": {
                "productTaxonomyNodeId": "gid://shopify/ProductTaxonomyNode/4134",
            },
            "metafields": [
                {
                    "key": "author",
                    "namespace": "book",
                    "value": self.author,
                },
                {
                    "key": "published_date",
                    "namespace": "book",
                    "value": self.published_date,
                },
                {
                    "key": "isbn",
                    "namespace": "facts",
                    "value": self.isbn,
                },
                {
                    "key": "staff_comment",
                    "namespace": "book",
                    "value": self.staff_comment,
                },
                {
                    "key": "backorder",
                    "namespace": "book",
                    "value": "true" if self.is_backorder else "false",
                },
            ],
        }
        if self.cover_image:
            data["images"] = [{"altText": self.title, "src": self.cover_image}]
        if self.location_ids:
            data["variants"][0]["inventoryPolicy"] = "CONTINUE"
            data["variants"][0]["inventoryQuantities"] = []
            for location_id in self.location_ids:
                if isinstance(location_id, int):
                    _location_id = location_id
                    _quantity = 0
                else:
                    _location_id, _quantity = location_id
                data["variants"][0]["inventoryQuantities"].append(
                    {
                        "locationId": f"gid://shopify/Location/{_location_id}",
                        "availableQuantity": _quantity,
                    }
                )
        if self.collection_ids:
            data["collectionsToJoin"] = [
                f"gid://shopify/Collection/{collection_id}"
                for collection_id in self.collection_ids
            ]
        return data


class UpdateBookInput(MutationSchema):
    product_id: int
    isbn: t.Optional[str] = None
    title: t.Optional[str] = None
    author: t.Optional[str] = None
    subtitle: t.Optional[str] = None
    description: t.Optional[str] = None
    publisher: t.Optional[str] = None
    published_date: t.Optional[str] = None

    @validator("isbn")
    def isbn_must_be_10_or_13_digits(cls, v):
        if v is None:
            return v
        if not is_valid_isbn(v):
            raise ValueError("ISBN must be 10 or 13 digits")
        return sanitize_isbn(v)


class MetafieldDefinition(QuerySchema):
    key: str
    name: str
    namespace: str
    description: t.Optional[str]


class MetafieldType(str, Enum):
    boolean = "boolean"
    collection_reference = "collection_reference"
    color = "color"
    date = "date"
    date_time = "date_time"
    dimension = "dimension"
    file_reference = "file_reference"
    json = "json"
    metaobject_reference = "metaobject_reference"
    mixed_reference = "mixed_reference"
    money = "money"
    multi_line_text_field = "multi_line_text_field"
    number_decimal = "number_decimal"
    number_integer = "number_integer"
    page_reference = "page_reference"
    product_reference = "product_reference"
    rating = "rating"
    single_line_text_field = "single_line_text_field"
    url = "url"
    variant_reference = "variant_reference"
    volume = "volume"
    weight = "weight"


class CreateMetafieldDefinitionInput(MutationSchema):
    name: str
    key: str
    type: MetafieldType
    namespace: str = "book"
    owner_type: str = "PRODUCT"

    def to_input_data(self) -> dict:
        return {
            "key": self.key,
            "type": self.type,
            "name": self.name,
            "ownerType": self.owner_type,
            "namespace": self.namespace,
        }


class Publication(QuerySchema):
    name: str
