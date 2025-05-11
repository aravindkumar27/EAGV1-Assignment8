import requests
import os
import httpx
import json

LAST_UPDATE_FILE = "last_update_id.json"

def get_last_update_id():
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("last_update_id", 0)
    return 0

def save_last_update_id(update_id):
    with open(LAST_UPDATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_update_id": update_id}, f)

async def get_latest_telegram_message() -> str:
    print("Inside get_latest_telegram_message() in telegram.py" )
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        print("Raw data from Telegram:", data)

        if "result" in data and data["result"]:
            # Get the latest update
            last_update = data["result"][-1]
            message = last_update.get("message", {}).get("text", "")
            
            # Mark update as read by using offset
            update_id = last_update["update_id"]
            await client.get(f"{url}?offset={update_id + 1}")
            print("Before return in if loop get_latest_telegram_message() in telegram.py")
            return message
        print("Before return outside if loop get_latest_telegram_message() in telegram.py")
        return "No messages"


def send_telegram_message(text: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    res = requests.post(url, data={"chat_id": chat_id, "text": text})
    return "Sent" if res.status_code == 200 else f"Failed to send: {res.text}"
