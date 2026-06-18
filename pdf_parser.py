from pypdf import PdfReader
from typing import Optional, Tuple

def parse_pdf_metadata_and_text(pdf_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the title and full text content from a local PDF file.

    Args:
        pdf_path: The full path to the PDF file.

    Returns:
        A tuple containing (title, text_content). Returns (None, None) if parsing fails.
    """
    title = None
    text_content = ""
    
    try:
        reader = PdfReader(pdf_path)
        
        # Attempt to get title from metadata first
        metadata = reader.metadata
        if metadata and metadata.title:
            title = metadata.title
        
        # Fallback: If metadata title is empty, try to use the filename as a title source
        if not title:
            # Clean up the filename to use as a title approximation
            title = os.path.splitext(os.path.basename(pdf_path))[0].replace("_", " ")
            
        # Extract text content from all pages
        full_text = []
        for page in reader.pages:
            full_text.append(page.extract_text() or "")
        
        text_content = "\n".join(full_text)

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
    
    return title, text_content