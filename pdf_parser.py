import os
from typing import Optional

from pypdf import PdfReader


def parse_pdf_metadata_and_text(pdf_path: str) -> tuple[Optional[str], Optional[str]]:
    title = None
    text_content = ""

    try:
        reader = PdfReader(pdf_path)

        metadata = reader.metadata
        if metadata and metadata.title:
            title = metadata.title

        if not title:
            title = os.path.splitext(os.path.basename(pdf_path))[0].replace("_", " ")

        text_content = "\n".join(page.extract_text() or "" for page in reader.pages)

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")

    return title, text_content
