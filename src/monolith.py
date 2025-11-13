import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import whisper

# Загружаем модель (tiny/base/small/medium/large)
model = whisper.load_model("large")

# Обработчик команды /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Привет, {user_first_name}! 👋\n"
        "Я могу распознавать голосовые сообщения на русском языке.\n"
        "Просто отправьте мне голосовое сообщение, и я верну текст!"
    )

# Обработчик голосовых сообщений
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.message.from_user.first_name
    await update.message.reply_text("Начинаю распознавание вашего голосового сообщения... ⏳")

    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    
    ogg_path = f"voice_{voice.file_id}.ogg"
    await file.download_to_drive(ogg_path)

    # Распознаем напрямую OGG (Whisper использует ffmpeg внутри)
    result = model.transcribe(
        ogg_path,
        language="ru",       # строго русский
        task="transcribe",   # просто распознавание, не перевод
        verbose=False        # отключает подробный вывод в консоль
    )

    await update.message.reply_text(f"Текст:\n{result['text']}")
    
    os.remove(ogg_path)

if __name__ == "__main__":
    load_dotenv()  # загружает переменные из .env
    TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Обработчики
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))

    print("✅ Бот успешно запущен!")
    app.run_polling()
