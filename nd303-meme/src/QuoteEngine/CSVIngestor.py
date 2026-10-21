"""Module for CSVIngestor class."""

from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

try:
    import pandas as pd
except ImportError:
    pd = None


class CSVIngestor(IngestorInterface):
    """Ingestor for CSV files containing quotes."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a CSV file.

        Args:
            path: Path to the CSV file.

        Returns:
            List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file: {path}")

        if pd is None:
            raise ImportError(
                "pandas library not installed; install via "
                "'pip install pandas'"
            )

        quotes = []

        try:
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                quotes.append(QuoteModel(str(row['body']), str(row['author'])))
        except Exception as e:
            raise RuntimeError(f"Error reading CSV file: {e}")

        return quotes
