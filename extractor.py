import re

from utils import extract_arxiv_identifiers, is_valid_arxiv_url


def extract_and_convert_urls(input_filepath: str) -> list[str]:
    print(f"Reading and analyzing input file: {input_filepath}")

    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return []
    except Exception as e:
        print(f"Error reading file {input_filepath}: {e}")
        return []

    arxiv_pattern = r"(https://arxiv\.org/abs/[a-zA-Z0-9\.\-\/]+)"
    raw_urls = re.findall(arxiv_pattern, content)

    if not raw_urls:
        print("No ArXiv URLs found in the input file.")
        return []

    print(f"Found {len(raw_urls)} potential ArXiv URLs.")

    seen = set()
    pdf_urls = []

    for url in raw_urls:
        if not is_valid_arxiv_url(url):
            continue
        identifier = extract_arxiv_identifiers(url)
        if identifier and identifier not in seen:
            seen.add(identifier)
            pdf_urls.append(url.replace("https://arxiv.org/abs/", "https://arxiv.org/pdf/"))

    return pdf_urls
