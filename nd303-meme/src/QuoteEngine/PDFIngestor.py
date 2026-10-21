"""Module for PDFIngestor class."""

import os
import subprocess
import tempfile
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingestor for PDF files containing quotes."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a PDF file using Xpdf pdftotext.

        Args:
            path: Path to the PDF file.

        Returns:
            List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file: {path}")

        quotes = []
        tmp_txt = None

        try:
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.txt', delete=False
            ) as f:
                tmp_txt = f.name

            result = subprocess.run(
                ['pdftotext', path, tmp_txt],
                check=True,
                capture_output=True,
                text=True
            )

            with open(tmp_txt, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if ' - ' in line:
                        body, author = line.split(' - ', 1)
                        quotes.append(QuoteModel(body.strip(), author.strip()))

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"pdftotext failed: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Xpdf pdftotext not installed; install via 'brew install xpdf'"
            )
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file: {e}")
        finally:
            if tmp_txt and os.path.exists(tmp_txt):
                os.remove(tmp_txt)

        return quotes
