import telebot

from config import TOKEN, MODEL_NAME
from utils.file_utils import save_file, cleanup_file
from services.whisper_service import recognize_voice

from services.obsidian_service import write_note, read_note

# Создаем экземпляр телебота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(
        message,
        f"Привет, {user_first_name}! 👋\n"
        "Я могу распознавать голосовые сообщения на русском языке.\n"
        "Просто отправьте мне голосовое сообщение!"
    )

# Обработчик команды /read
@bot.message_handler(commands=['read'])
def read_note_handler(message):
    content = read_note()
    if content is None:
        bot.reply_to(message, "❌ Файл не найден! Проверь VAULT_PATH.")
    else:
        bot.reply_to(message, f"📄 Содержимое файла:\n\n{content}")



# Обработчик голосовых сообщений
    # @bot.message_handler(content_types=['voice'])
    # def voice_handler(message):
    #     bot.reply_to(message, "Начинаю распознавание вашего голосового сообщения... ⏳")
    #     file_path = save_file(bot, message.voice.file_id)
    #     text = recognize_voice(file_path, language="ru")
    #     bot.reply_to(message, f"📄 Распознанный текст:\n\n{text}")
    #     cleanup_file(file_path)
@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    sent_msg = bot.send_message(message.chat.id, "Начинаю распознавание вашего голосового сообщения... ⏳") # Отправляем первое сообщение
    file_path = save_file(bot, message.voice.file_id) # Сохраняем голосовой файл
    text = recognize_voice(file_path, language="ru")  # Распознаём текст
    bot.edit_message_text(                            # Изменяем текст отправленного сообщения
        chat_id=sent_msg.chat.id,
        message_id=sent_msg.message_id,
        text=f"📄 Распознанный текст:\n\n{text}"
    )
    cleanup_file(file_path) # Убираем временный файл
    write_note(text)



print(f"✅ Бот успешно запущен с моделью {MODEL_NAME}!")
bot.polling(none_stop=True)
