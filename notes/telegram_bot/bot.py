import requests
from .config import BOT_TOKEN, TELEGRAM_CHAT_ID


def send_note_to_telegram(note):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    categories = ", ".join(
        category.name_categories for category in note.categories.all()
    ) or "Без категорії"

    message = (
        f"Нова нотатка\n\n"
        f"Назва: {note.title}\n"
        f"Текст: {note.text}\n"
        f"Категорії: {categories}\n"
    )

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    response = requests.post(url, data=data, timeout=15)
    print("TELEGRAM STATUS:", response.status_code)
    print("TELEGRAM BODY:", response.text)
    response.raise_for_status()

    return response.json()