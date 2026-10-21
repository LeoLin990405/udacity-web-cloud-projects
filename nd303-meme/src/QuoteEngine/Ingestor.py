"""Module for Ingestor class (dispatcher)."""

from typing import List
from .IngestorInterface import IngestorInterface
from .TextIngestor import TextIngestor
from .DocxIngestor import DocxIngestor
from .CSVIngestor import CSVIngestor
from .PDFIngestor import PDFIngestor
from .QuoteModel import QuoteModel


class Ingestor(IngestorInterface):
    """Ingestor dispatcher that selects the appropriate ingestor for a file."""

    ingestors = [TextIngestor, DocxIngestor, CSVIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a file using the appropriate ingestor.

        Args:
            path: Path to the file.

        Returns:
            List of QuoteModel objects.

        Raises:
            ValueError: If no matching ingestor is found for the file.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No matching ingestor for path: {path}")
