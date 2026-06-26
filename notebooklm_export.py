import asyncio

_PDF_PREFIX = "https://arxiv.org/pdf/"
_DELAY = 5  # ponytail: rate limit mitigation between source uploads


def has_auth() -> bool:
    from notebooklm.paths import get_storage_path
    return get_storage_path().exists()


def export(arxiv_ids, title="ArXiv Papers") -> None:
    """Runs in a background thread."""
    asyncio.run(_run(arxiv_ids, title))


async def _run(arxiv_ids, title):
    from notebooklm import NotebookLMClient

    urls = [f"{_PDF_PREFIX}{aid}.pdf" for aid in arxiv_ids]
    try:
        async with NotebookLMClient.from_storage() as client:
            notebook = await client.notebooks.create(title)
            for url in urls:
                await client.sources.add_url(notebook.id, url)
                await asyncio.sleep(_DELAY)
        print(f"[NotebookLM] notebook '{title}' created with {len(urls)} sources")
    except Exception as e:
        print(f"[NotebookLM] export failed: {e}")
        raise
