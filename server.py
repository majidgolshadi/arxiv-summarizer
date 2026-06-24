import json
import shutil
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import config

_HTML_PATH = Path(__file__).parent / "index.html"


class _Handler(BaseHTTPRequestHandler):
    summary_dir = None
    date_dir = None

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html; charset=utf-8", _HTML_PATH.read_bytes())
        elif self.path == "/summaries":
            data = self._load_summaries()
            self._send(200, "application/json", json.dumps(data, ensure_ascii=False).encode())
        else:
            self._send(404, "text/plain", b"Not Found")

    def do_POST(self):
        if self.path == "/archive":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            result = self._archive(body.get("ids", []))
            self._send(200, "application/json", json.dumps(result).encode())
        else:
            self._send(404, "text/plain", b"Not Found")

    def _archive(self, ids):
        archived_dir = Path(self.date_dir) / "archived"
        archived_dir.mkdir(exist_ok=True)
        count = 0
        not_found = []
        for arxiv_id in ids:
            src = Path(self.date_dir) / f"{arxiv_id}.pdf"
            if src.exists():
                shutil.copy2(src, archived_dir / src.name)
                count += 1
            else:
                not_found.append(arxiv_id)
        return {"archived": count, "not_found": not_found}

    def _load_summaries(self):
        result = []
        for p in sorted(Path(self.summary_dir).glob("*.txt")):
            content = p.read_text(encoding="utf-8")
            title = content.split("\n", 1)[0].strip() or p.stem
            result.append({"id": p.stem, "title": title, "content": content})
        return result

    def _send(self, code, ctype, body):
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
