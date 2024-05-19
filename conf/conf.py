import os

from dotenv import load_dotenv
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
load_dotenv(f"{BASE_PATH}/.env")


class BotConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN = os.getenv("ADMIN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")


class Conf:
    bot = BotConfig()
