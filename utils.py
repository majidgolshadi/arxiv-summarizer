import datetime
import os
import re

def get_date_directory():
    """Generates the execution date directory name in YYYY_mon_DD format."""
    today = datetime.datetime.now()
    # Format month to be 2 digits (e.g., 06)
    return today.strftime("%Y_%b_%d").replace(" ", "_").title()

def sanitize_filename(text):
    """Sanitizes a string to be used as a filesystem name."""
    # Keep alphanumeric characters, spaces, and hyphens
    # Replace everything else with nothing
    return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')

def is_valid_arxiv_url(url):
    """Checks if the URL is a valid ArXiv abstract URL."""
    return bool(re.match(r'https://arxiv\.org/abs/[0-9]{4}\.[0-9]{4}', url))

def extract_arxiv_identifiers(url):
    """Extracts the unique identifier (e.g., 2501.12345) from a valid ArXiv URL."""
    match = re.search(r'arxiv\.org/abs/(\S+)', url)
    if match:
        return match.group(1)
    return None