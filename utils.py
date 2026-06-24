import datetime
import re


def get_date_directory():
    return datetime.datetime.now().strftime("%Y_%b_%d").title()


def is_valid_arxiv_url(url):
    return bool(re.match(r'https://arxiv\.org/abs/[0-9]{4}\.[0-9]{4}', url))


def extract_arxiv_identifiers(url):
    match = re.search(r'arxiv\.org/abs/(\S+)', url)
    return match.group(1) if match else None
