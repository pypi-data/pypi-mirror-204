from __future__ import annotations

from typing import List

from .schema import MetafieldDefinition, ShopifyBook, ShopifyShop


def to_shopify_shop(payload: dict) -> ShopifyShop:
    """
    Parses a dictionary and creates a ShopifyShop object from the data.

    This function takes a dictionary as input and creates a ShopifyShop object from the data in the dictionary.
    The dictionary should contain "id", "name", and "myshopifyDomain" fields.

    Parameters:
    payload (dict): The dictionary to parse.

    Returns:
    ShopifyShop: A ShopifyShop object created from the data in the dictionary.

    Raises:
    ValueError: If the dictionary is not in the expected format.
    """
    try:
        return ShopifyShop(
            gid=payload["id"],
            name=payload["name"],
            myshopify_domain=payload["myshopifyDomain"],
        )
    except KeyError:
        raise ValueError(
            "Dictionary does not contain expected 'id', 'name', and 'myshopifyDomain' fields"
        )


def to_shopify_book(payload: dict) -> ShopifyBook:
    def _find_value(metafields: List[dict], key: str) -> any:
        for metafield in metafields:
            if metafield["node"]["key"] == key:
                return metafield["node"]["value"]
        return None

    try:
        try:
            metafields = payload["metafields"]["edges"]
        except KeyError:
            metafields = payload["metafields"]
        variant = payload["variants"]["edges"][0]["node"]
        return ShopifyBook(
            gid=payload["id"],
            isbn=variant["sku"],
            title=payload["title"],
            price=variant["price"],
            subtitle="",
            author=_find_value(metafields, "author"),
            description=payload["descriptionHtml"],
            publisher=payload["vendor"],
            published_date=_find_value(metafields, "published_date"),
        )
    except KeyError:
        raise ValueError(
            "Dictionary does not contain expected 'id', 'title', 'author', 'descriptionHtml', and 'vendor' fields"
        )


def to_metafield_definition(payload: dict) -> MetafieldDefinition:
    """
    Parses a dictionary and creates a Metafield object from the data.

    This function takes a dictionary as input and creates a Metafield object from the data in the dictionary.
    The dictionary should contain "id", "namespace", "key", and "value" fields.

    Parameters:
    payload (dict): The dictionary to parse.

    Returns:
    Metafield: A Metafield object created from the data in the dictionary.

    Raises:
    ValueError: If the dictionary is not in the expected format.
    """
    try:
        return MetafieldDefinition(
            name=payload["name"],
            namespace=payload["namespace"],
            key=payload["key"],
        )
    except KeyError:
        raise ValueError(
            "Dictionary does not contain expected 'namespace', 'key', and 'value' fields"
        )
