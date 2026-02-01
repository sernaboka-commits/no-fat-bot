import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables")

if not BASE_URL:
    raise RuntimeError("BASE_URL is not set in environment variables")
