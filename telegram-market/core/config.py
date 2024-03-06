import os
from dotenv import load_dotenv
load_dotenv(".env")


BOT_TOKEN = os.getenv("ENV_BOT_TOKEN")
BOT_LINK = os.getenv("ENV_BOT_LINK")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
YANDEX_ACQUIRING_SECRET_KEY = os.getenv("ENV_YANDEX_ACQUIRING_SECRET_KEY")
YANDEX_ACQUIRING_IDENTIFIER = os.getenv("ENV_YANDEX_ACQUIRING_IDENTIFIER")
YANDEX_AUTH = (YANDEX_ACQUIRING_IDENTIFIER, YANDEX_ACQUIRING_SECRET_KEY)
CHANNEL_CHAT_ID = "-1002120517067"
CHANNEL_NAME = "Vivaldi"
API_BASE_URL = os.getenv("ENV_API_BASE_URL")
STATIC_PICS = "static/pics/"


START_MENU = ["main_menu"]
BACK_BUTTON_TEXT = "🔙 Back"
MAIN_BUTTON_TEXT = "<< Main Ⓜ️"
ARROW_LEFT = "⬅️"
ARROW_RIGHT = "➡️"
REPLY_TO_USER = "Hi there,<b>%USERNAME%!</b>\n"
REPLY_TO_NOTSUBSCRIBED = "You ain't subscribed on channel: %CHANNEL%\nSubscribe to unlock functions"
REPLY_TO_MANAGER = "Hi there manager! nice to see you, %USERNAME%!"
