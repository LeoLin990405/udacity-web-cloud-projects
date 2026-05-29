"""QuoteEngine module for ingesting quotes from various file formats."""

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
from .TextIngestor import TextIngestor
from .DocxIngestor import DocxIngestor
from .CSVIngestor import CSVIngestor
from .PDFIngestor import PDFIngestor
from .Ingestor import Ingestor

__all__ = [
    'QuoteModel',
    'IngestorInterface',
    'TextIngestor',
    'DocxIngestor',
    'CSVIngestor',
    'PDFIngestor',
    'Ingestor'
]
