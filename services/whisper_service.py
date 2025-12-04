import whisper
from config import MODEL_NAME


# Загружаем модель один раз
model = whisper.load_model(MODEL_NAME)

def recognize_voice(file_path: str, language: str = "ru") -> str:
    # Распознаёт аудио с помощью модели Whisper.
    result = model.transcribe(
        file_path,
        language=language,
        task="transcribe",
        verbose=False
    )
    return result["text"]

