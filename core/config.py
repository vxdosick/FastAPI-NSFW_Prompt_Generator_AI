import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
STRIPE_LIVE_SECRET_KEY = os.getenv("STRIPE_LIVE_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_LIVE_WEBHOOK_SECRET = os.getenv("STRIPE_LIVE_WEBHOOK_SECRET")