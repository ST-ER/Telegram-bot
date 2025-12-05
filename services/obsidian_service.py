import subprocess
from pathlib import Path
from config import VAULT_PATH

def push_to_github():
    """
    Добавляет все изменения в git, делает коммит и пушит на GitHub.
    """
    try:
        # Переходим в папку ObsidianVault
        repo_path = VAULT_PATH
        subprocess.run(["git", "-C", str(repo_path), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo_path), "commit", "-m", "Update vault via Telegram bot"], check=True)
        subprocess.run(["git", "-C", str(repo_path), "push", "origin", "main"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Git push failed:", e)
        return False

# def read_note() -> str | None:
#     """Чтение содержимого файла (если существует)."""
#     if not VAULT_PATH.exists():
#         return None
#     with open(VAULT_PATH, "r", encoding="utf-8") as f:
#         return f.read()

# def write_note(text: str):
#     with open(VAULT_PATH, "w", encoding="utf-8") as f:
#         f.write(text)