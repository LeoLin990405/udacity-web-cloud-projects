"""Module for DocxIngestor class."""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

try:
    from docx import Document
except ImportError:
    Document = None


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files containing quotes."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a DOCX file.

        Args:
            path: Path to the DOCX file.

        Returns:
            List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file: {path}")

        if Document is None:
            raise ImportError(
                "python-docx library not installed; install via "
                "'pip install python-docx'"
            )

        quotes = []

        try:
            doc = Document(path)
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                if ' - ' in text:
                    body, author = text.split(' - ', 1)
                    quotes.append(QuoteModel(body.strip(), author.strip()))
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX file: {e}")

        return quotes
