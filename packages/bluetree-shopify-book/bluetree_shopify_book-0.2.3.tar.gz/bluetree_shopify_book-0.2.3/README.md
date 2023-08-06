# Shopify Book Service

The Shopify Book Service is a Python library for managing books in a Shopify store. It provides a simple interface for performing CRUD (Create, Read, Update, Delete) operations on books, as well as for setting up and managing metafields for books.

## Installation

To install the Shopify Book Service, run the following command:

`pip install bluetree-shopify-book`

## Usage

To use the Shopify Book Service, you first need to create an instance of the ShopifyBookService class with your shop's URL and API access token:

```
from bluetree_shopify_book import ShopifyBookService

shop_url = "https://yourshopdomain.myshopify.com"
admin_api_access_token = "YOUR_ACCESS_TOKEN"

book_service = ShopifyBookService(shop_url, admin_api_access_token)
```

Note that the ShopifyBookService class uses a context manager, so you can use it in a with statement to automatically activate and clear the Shopify session:

```
with ShopifyBookService(shop_url, admin_api_access_token) as book_service:
    # do something with book_service
```

## Getting a Book

To get a book by ID, use the get_book_by_id() method:

```
book = book_service.get_book_by_id(8148173881647)
```

To get a book by ISBN, use the get_book_by_isbn() method:

```
book = book_service.get_book_by_isbn("9780141439846")
```

## Creating a Book

To create a book, use the create_book() method:

```
from src.schema import CreateBookInput

book_input = CreateBookInput(
    title="Pride and Prejudice",
    author="Jane Austen",
    description="A classic novel about love and social status.",
    price="12.99",
    sku="9780141439846",
    published_date="1813-01-28",
)

book = book_service.create_book(book_input)
```

## To create multiple books concurrently, use the create_books() method:

```
from src.schema import CreateBookInput

book_inputs = [
    CreateBookInput(
        title="Pride and Prejudice",
        author="Jane Austen",
        description="A classic novel about love and social status.",
        price="12.99",
        sku="9780141439846",
        published_date="1813-01-28",
    ),
    CreateBookInput(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        description="A powerful novel about race and justice in the American South.",
        price="14.99",
        sku="9780061120084",
        published_date="1960-07-11",
    ),
]

books = book_service.create_books(book_inputs)
```

## Updating a Book

To update a book's price, use the update_book_price() method:

```
from decimal import Decimal

book_variant_id = 1234567890
new_price = Decimal("14.99")

book = book_service.update_book_price(book_variant_id, new_price)
```

## Deleting a Book

To delete a book, use the delete_book() method:

```
book_id = 1234567890

book_service.delete_book(book_id)
```

## Setting up Metafield Definitions

To set up default metafield definitions for books, use the setup_default_metafield_definitions() method:

```
book_service.setup_default_metafield_definitions()
```

## Getting Metafield Definitions

To get all metafield definitions for books, use the _get_metafield_definitions() method:

```
metafield_definitions = book_service
```