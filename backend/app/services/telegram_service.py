import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def send_telegram_message(text: str):
    if not ADMIN_CHAT_ID or not BOT_TOKEN  :
        print("The telegram key doesn't found in .env")
        return

    
    url= f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Notification success send in the Telegram")
    except Exception as e:
        print(f"Error: {e}")
