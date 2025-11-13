import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import whisper
from transcriber import transcribe_audio, cleanup_file

# Загружаем модель один раз и передаем её в функцию
MODEL_NAME = "medium"
model = whisper.load_model(MODEL_NAME)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Привет, {user_first_name}! 👋\n"
        "Я могу распознавать голосовые сообщения на русском языке.\n"
        "Просто отправьте мне голосовое сообщение, и я верну текст!"
    )

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Начинаю распознавание вашего голосового сообщения... ⏳")

    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    
    ogg_path = f"voice_{voice.file_id}.ogg"
    await file.download_to_drive(ogg_path)

    # Передаем модель и путь к файлу в модуль
    text = transcribe_audio(ogg_path, model=model, language="ru")
    await update.message.reply_text(f"Текст:\n{text}")

    cleanup_file(ogg_path)

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))

    print(f"✅ Бот успешно запущен с моделью {MODEL_NAME}!")
    app.run_polling()
