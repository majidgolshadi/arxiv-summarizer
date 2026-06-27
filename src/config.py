import yaml
from pathlib import Path

_cfg = yaml.safe_load((Path(__file__).parent.parent / "config" / "config.yaml").read_text())

OLLAMA_API_URL = _cfg["ollama_api_url"]
MODEL_NAME = _cfg["model_name"]
MAX_TEXT_CHARS = _cfg["max_text_chars"]
LANGUAGE = _cfg["language"]
WORD_COUNT_HINTS = _cfg["word_count_hints"]
DATA_DIR = _cfg["data_dir"]
SERVER_PORT = _cfg["server_port"]
NOTEBOOKLM_EXPORT = _cfg.get("notebooklm_export", False)
