# Imports
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from telegram import Update, Bot
import os, stripe
from storage.storage import load_users, save_users
from bot.bot import app as tg_app, bot

# Load dotenv variables
load_dotenv()

# Define tokens
stripe.api_key=os.getenv("STRIPE_LIVE_SECRET_KEY")

# Project initialisation
async def init_telegram():
    await bot.initialize()
    await tg_app.initialize()

@asynccontextmanager
async def lifespan(server: FastAPI):
    await init_telegram()
    yield

# FastAPI server creating
server = FastAPI(lifespan=lifespan)

# FastAPI Endpoints
@server.post("/create-checkout-session/{user_id}")
async def create_checkout(user_id: str):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": "10 Credits",
                },
                "unit_amount": 50,
            },
            "quantity": 1,
        }],
        mode="payment",
        # save user information
        payment_intent_data= {
            "metadata": {
            "telegram_user_id": user_id,
            "credits": "10"
            },
        },
        success_url="https://t.me/nsfw_prompt_generator_bot?start=payment_success",
        cancel_url="https://t.me/nsfw_prompt_generator_bot?start=payment_cancel"
    )
    return {"url": session.url}

# ------------------------------
# Stripe webhook
# ------------------------------
@server.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    print("=== WEBHOOK RECEIVED ===")
    print("Headers:", request.headers)
    print("Payload length:", len(payload))

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        print("WEBHOOK ERROR:", e)
        raise HTTPException(status_code=400)

    if event["type"] == "payment_intent.succeeded":
        pi = event["data"]["object"]

        telegram_user_id = pi["metadata"].get("telegram_user_id")
        credits = int(pi["metadata"].get("credits", 0))

        print("PAYMENT OK:", telegram_user_id, credits)

        users = load_users()
        users.setdefault(telegram_user_id, {"credits": 0})
        users[telegram_user_id]["credits"] += credits
        save_users(users)

    return {"status": "ok"}

# ------------------------------
# Telegram webhook
# ------------------------------
@server.post("/tg-webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    update = Update.de_json(payload, bot)
    await tg_app.process_update(update)
    return {"ok": True}