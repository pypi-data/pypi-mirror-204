from __future__ import annotations


class BookNotFound(Exception):
    """
    Exception raised when a book is not found.

    This exception is raised when a book cannot be found in a database or data store.
    """

    pass


class BookAlreadyExists(Exception):
    """
    Exception raised when a book already exists.

    This exception is raised when a book with the same name or ISBN already exists in a database or data store.
    """

    pass
