import os
from config import VOICE_FOLDER
from telebot import TeleBot

def save_file(bot: TeleBot, file_id: str) -> str:
    # Скачивает голосовое сообщение с Telegram и сохраняет локально.
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    os.makedirs(VOICE_FOLDER, exist_ok=True)
    file_path = f"{VOICE_FOLDER}/{file_id}.ogg"

    with open(file_path, 'wb') as f:
        f.write(downloaded)

    return file_path

def cleanup_file(file_path: str):
    # Удаляет файл с диска, если он существует.
    if os.path.exists(file_path):
        os.remove(file_path)
