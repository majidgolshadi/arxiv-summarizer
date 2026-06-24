import datetime
import re


def get_date_directory():
    return datetime.datetime.now().strftime("%Y_%b_%d").title()


def get_latest_directory(base_dir):
    from pathlib import Path
    base_path = Path(base_dir)
    if not base_path.exists() or not base_path.is_dir():
        return None

    subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    if not subdirs:
        return None

    # Sort by modification time to get the latest directory
    latest_dir = max(subdirs, key=lambda d: d.stat().st_mtime)
    return latest_dir.name


def is_valid_arxiv_url(url):
    return bool(re.match(r'https://arxiv\.org/abs/[0-9]{4}\.[0-9]{4}', url))


def extract_arxiv_identifiers(url):
    match = re.search(r'arxiv\.org/abs/(\S+)', url)
    return match.group(1) if match else None
