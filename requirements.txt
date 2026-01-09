import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def get_updates(offset=None):
    url = BASE_URL + "/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        r = requests.get(url, params=params, timeout=40)
        return r.json()
    except:
        return {"result": []}


def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": text
        }, timeout=20)
    except:
        pass


def ask_ai(text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Ты умный и дружелюбный помощник. Отвечай кратко и понятно."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 400
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        j = r.json()
        return j["choices"][0]["message"]["content"]
    except:
        return "⚠️ Ошибка ИИ. Попробуй позже."


def main():
    print("🤖 Бот запущен")
    offset = None

    while True:
        updates = get_updates(offset)

        for update in updates.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text.strip() == "":
                continue

            send_message(chat_id, "🤔 Думаю...")
            answer = ask_ai(text)
            send_message(chat_id, answer)

        time.sleep(1)


if __name__ == "__main__":
    main()
