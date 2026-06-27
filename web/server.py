import json
import shutil
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from src import config
from src import notebooklm_export

if config.NOTEBOOKLM_EXPORT:
    pass

_HTML_PATH = Path(__file__).parent / "index.html"


# ── Archive file operation ───────────────────────────────────────────────────

def _copy_to_archive(ids: list, date_dir: str) -> tuple[list, list]:
    """Copy selected PDFs into the archive subdirectory.

    Returns (archived_ids, not_found_ids).
    """
    archive_dir = Path(date_dir) / "archived"
    archive_dir.mkdir(exist_ok=True)
    archived, not_found = [], []
    for arxiv_id in ids:
        src = Path(date_dir) / f"{arxiv_id}.pdf"
        if src.exists():
            shutil.copy2(src, archive_dir / src.name)
            archived.append(arxiv_id)
        else:
            not_found.append(arxiv_id)
    return archived, not_found


# ── Post-archive pipeline ────────────────────────────────────────────────────
# After files are archived, each registered step runs in sequence.
# Each step receives (archived_ids, date_dir) and returns a status string.
#
# To add a new step:
#   1. Define a function: def _my_step(ids, date_dir) -> str
#   2. Append it:         _POST_ARCHIVE_STEPS.append(("my_step", _my_step))

def _notebooklm_step(ids: list, date_dir: str) -> str:
    """Export archived PDFs to a new Google NotebookLM notebook."""
    if not notebooklm_export.has_auth():
        return "needs_auth"
    date_label = Path(date_dir).name.replace("_", " ")
    threading.Thread(
        target=notebooklm_export.export,
        args=(ids, f"AI - arXiv - {date_label}"),
        daemon=True,
    ).start()
    return "started"


_POST_ARCHIVE_STEPS = []

if config.NOTEBOOKLM_EXPORT:
    _POST_ARCHIVE_STEPS.append(("notebooklm", _notebooklm_step))


# ── HTTP server ──────────────────────────────────────────────────────────────

class _Handler(BaseHTTPRequestHandler):
    summary_dir = None
    date_dir = None

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html; charset=utf-8", _HTML_PATH.read_bytes())
        elif self.path == "/summaries":
            summaries = self._load_summaries()
            self._send(200, "application/json",
                       json.dumps(summaries, ensure_ascii=False).encode())
        else:
            self._send(404, "text/plain", b"Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        if self.path == "/archive":
            result = self._handle_archive(body.get("ids", []))
            self._send(200, "application/json", json.dumps(result).encode())
        else:
            self._send(404, "text/plain", b"Not Found")

    def _handle_archive(self, ids: list) -> dict:
        archived_ids, not_found = _copy_to_archive(ids, self.date_dir)

        step_results = {}
        if archived_ids:
            for name, step in _POST_ARCHIVE_STEPS:
                step_results[name] = step(archived_ids, self.date_dir)

        return {"archived": len(archived_ids), "not_found": not_found, **step_results}

    def _load_summaries(self) -> list:
        summaries = []
        for path in sorted(Path(self.summary_dir).glob("*.txt")):
            content = path.read_text(encoding="utf-8")
            title = content.split("\n", 1)[0].strip() or path.stem
            summaries.append({"id": path.stem, "title": title, "content": content})
        return summaries

    def _send(self, code: int, ctype: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


def start_server(summary_dir, port=config.SERVER_PORT):
    _Handler.summary_dir = str(summary_dir)
    _Handler.date_dir = str(Path(summary_dir).parent)
    server = HTTPServer(("localhost", port), _Handler)
    url = f"http://localhost:{port}"
    print(f"\n[SERVER] Summaries available at {url}  (Ctrl+C to stop)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Stopped.")
