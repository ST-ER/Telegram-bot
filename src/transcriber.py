import os

def transcribe_audio(file_path: str, model, language: str = "ru") -> str:
    """
    Распознаёт речь из аудиофайла с помощью переданной модели Whisper.
    
    Args:
        file_path (str): путь к аудиофайлу (ogg, mp3, wav и др.)
        model: объект whisper.Model, загруженная модель
        language (str): язык распознавания, по умолчанию "ru"
        
    Returns:
        str: распознанный текст
    """
    result = model.transcribe(
        file_path,
        language=language,
        task="transcribe",
        verbose=False
    )
    return result["text"]

def cleanup_file(file_path: str):
    """Удаляет файл с диска, если он существует."""
    if os.path.exists(file_path):
        os.remove(file_path)
