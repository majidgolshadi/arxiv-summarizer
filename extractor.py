import re
from utils import is_valid_arxiv_url, extract_arxiv_identifiers

def extract_and_convert_urls(input_filepath: str) -> list[str]:
    """
    Scans the input text file for ArXiv URLs, extracts unique identifiers,
    and converts them from abstract format to direct PDF download format.
    """
    print(f"Reading and analyzing input file: {input_filepath}")
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return []
    except Exception as e:
        print(f"Error reading file {input_filepath}: {e}")
        return []

    # Regex to find any potential ArXiv URLs
    # This pattern is broad and will capture the full URL.
    arxiv_pattern = r'(https://arxiv\.org/abs/[a-zA-Z0-9\.\-\/]+)'
    
    raw_urls = re.findall(arxiv_pattern, content)
    
    if not raw_urls:
        print("No ArXiv URLs found in the input file.")
        return []

    unique_identifiers = set()
    pdf_urls = set()

    print(f"Found {len(raw_urls)} potential ArXiv URLs.")
    
    for url in raw_urls:
        if is_valid_arxiv_url(url):
            # 1. Extract the unique identifier (e.g., 2501.12345)
            identifier = extract_arxiv_identifiers(url)
            if identifier and identifier not in unique_identifiers:
                unique_identifiers.add(identifier)
                
                # 2. Convert URL from /abs/ format to /pdf/ format
                # Original: https://arxiv.org/abs/2501.12345
                # Target:   https://arxiv.org/pdf/2501.12345
                pdf_url = url.replace("https://arxiv.org/abs/", "https://arxiv.org/pdf/")
                pdf_urls.add(pdf_url)
            else:
                # This handles potential duplicates already processed
                pass

    return list(pdf_urls)