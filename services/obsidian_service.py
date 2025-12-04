from pathlib import Path
from config import VAULT_PATH

def read_note() -> str | None:
    """Чтение содержимого файла (если существует)."""
    if not VAULT_PATH.exists():
        return None
    with open(VAULT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_note(text: str):
    with open(VAULT_PATH, "w", encoding="utf-8") as f:
        f.write(text)