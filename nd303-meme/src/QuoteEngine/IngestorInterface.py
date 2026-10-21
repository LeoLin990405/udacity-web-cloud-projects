"""Module for IngestorInterface abstract base class."""

from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Abstract base class for quote ingestors."""

    allowed_extensions: list = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file can be ingested by this ingestor.

        Args:
            path: Path to the file.

        Returns:
            True if file extension is in allowed_extensions, False otherwise.
        """
        ext = path.split('.')[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a file.

        Args:
            path: Path to the file.

        Returns:
            List of QuoteModel objects.
        """
        pass
