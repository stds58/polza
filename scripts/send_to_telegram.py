"""
Мини-интеграция с Telegram
Сделать небольшой скрипт или n8n-флоу, который:
• принимает текст из файла .txt;
• отправляет этот текст в выбранный приватный Telegram-чат через Telegram-бота.
UI не нужен. Красивый код тоже не нужен. Главное — чтобы работало.
"""
import requests
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str


settings = Settings()


def send_message_to_telegram(chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    data = response.json()
    return data

def main(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return send_message_to_telegram(chat_id=settings.TELEGRAM_CHAT_ID, message=content)
    except FileNotFoundError:
        return ("Файл %s не найден" % filename)


if __name__ == "__main__":
    result = main('scripts/message.txt')
    print(result)
