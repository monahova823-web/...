import requests
import time

TELEGRAM_TOKEN = "8046920819:AAEXHdGVfw7yVvAMxxNXXrQY-WeNxMr-V44"
OPENAI_API_KEY =""

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def get_updates(offset=None):
    try:
        url = BASE_URL + "/getUpdates"
        params = {"timeout": 30, "offset": offset}
        r = requests.get(url, params=params, timeout=40)
        data = r.json()
        return data.get("result", [])
    except Exception as e:
        print("Ошибка getUpdates:", e)
        return []


def send_message(chat_id, text):
    try:
        url = BASE_URL + "/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=20)
    except Exception as e:
        print("Ошибка sendMessage:", e)


def ask_ai(text):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Ты полезный ИИ-помощник, отвечай по-русски."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 300
        }

        r = requests.post(url, headers=headers, json=data, timeout=60)
        response = r.json()

        if "choices" not in response:
            print("Ответ OpenAI без choices:", response)
            return "⚠️ ИИ временно недоступен, попробуй позже."

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print("Ошибка OpenAI:", e)
        return "⚠️ Ошибка ИИ. Попробуй ещё раз."


def main():
    offset = None
    print("Бот запущен ✅")

    while True:
        updates = get_updates(offset)

        for update in updates:
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            chat = message.get("chat")
            if not chat:
                continue

            chat_id = chat.get("id")
            text = message.get("text")

            if not text:
                continue

            if text.strip() == "":
                send_message(chat_id, "❗ Напиши сообщение текстом")
                continue

            send_message(chat_id, "🤖 Думаю...")

            reply = ask_ai(text)
            send_message(chat_id, reply)

        time.sleep(1)


if __name__ == "__main__":
    main()
