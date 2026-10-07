import os
from dotenv import load_dotenv

# Load variables from the root .env file
load_dotenv()

TOKEN = os.getenv("Telegram_Bot_Token")
if not TOKEN:
    raise ValueError("Telegram_Bot_Token is missing from your .env file!")
