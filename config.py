import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   # Телеграм токен
MODEL_NAME = "medium"                     # Модель Whisper
VOICE_FOLDER = "data"                     # Папка для временных файлов
VAULT_PATH = Path("../ObsidianVault")

