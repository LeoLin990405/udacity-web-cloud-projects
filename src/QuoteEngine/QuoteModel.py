"""Module for QuoteModel class."""


class QuoteModel:
    """A class to represent a quote with a body and author."""

    def __init__(self, body: str, author: str):
        """Initialize QuoteModel with body and author.

        Args:
            body: The text of the quote.
            author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return string representation for debugging."""
        return f"QuoteModel(body={self.body!r}, author={self.author!r})"

    def __str__(self):
        """Return human-readable string representation."""
        return f'"{self.body}" - {self.author}'
