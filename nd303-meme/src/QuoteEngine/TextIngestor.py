"""Module for TextIngestor class."""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """Ingestor for text files containing quotes."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a text file.

        Args:
            path: Path to the text file.

        Returns:
            List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file: {path}")

        quotes = []

        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if ' - ' in line:
                        body, author = line.split(' - ', 1)
                        quotes.append(QuoteModel(body.strip(), author.strip()))
        except Exception as e:
            raise RuntimeError(f"Error reading text file: {e}")

        return quotes
