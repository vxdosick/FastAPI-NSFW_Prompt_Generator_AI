# Imports
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram import Bot
from dotenv import load_dotenv
from openai import OpenAI
import os, time, httpx, sys

# Dotenv, storage path connecting
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.storage import load_users, save_users, START_CREDITS

# Define tokens
TOKEN = os.getenv("TB_TOKEN")
SERVER_URL = os.getenv('SERVER_URL')

# TB App creating
bot = Bot(TOKEN)
app = Application.builder().token(TOKEN).build()

# Functions
user_last_action = {}
def is_rate_limited(user_id, cooldown=3):
    now = time.time()
    last = user_last_action.get(user_id, 0)
    if now - last < cooldown:
        return True
    
    user_last_action[user_id] = now
    return False

# Requests (functions in telegram)
async def start(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    
    user_id = str(update.effective_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "credits": START_CREDITS
        }
        save_users(users)

    await update.message.reply_text(f"""!ТУТ БУДЕТ ПРИВЕТСТВИЕ, ПРЕДНАЗНАЧЕНИЕ БОТА И ФУНКЦИИ
                                    (КРЕДИТОВ ОСТАЛОСЬ: {users[user_id]["credits"]})""")

async def help(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    await update.message.reply_text("!ТУТ БУДЕТ ИНФОРМАЦИЯ О БОТЕ, ПОМОЩЬ ГРУБО ГОВОРЯ")

async def credits(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    user_id = str(update.effective_user.id)
    users = load_users()

    credits = users.get(user_id, {}).get("credits", 0)

    await update.message.reply_text(f"У ПОЛЬЗОВАТЕЛЯ ОСТАЛОСЬ {credits} КРЕДИТОВ")

async def buy(update, context):
    user_id = str(update.effective_user.id)

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVER_URL}/create-checkout-session/{user_id}")
        data = r.json()
        await update.message.reply_text(f"КУПИ 10 КРЕДИТОВ ПУПСИК - {data['url']}")

async def unknown(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    await update.message.reply_text("!ТУТ БУДЕТ ТЕКСТ НЕИЗВЕСНОЙ КОМАНДЫ, СПИСОК КОМАНД")

# Requests (text in telegram)
async def echo(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    
    user_id = str(update.effective_user.id)
    users = load_users()
    
    if is_rate_limited(user_id):
        await update.message.reply_text("!ТУТ БУДЕТ ТЕКСТ ОБОЗНАЧАЮЩИЙ СЛИШЬКОМ ЧАСТЫЕ ЗАПРОСЫ")
        return
    
    # request to GPT 4o-mini
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
        extra_body={},
        model="openai/gpt-4o-mini",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Take on the role of a prompt generator.
                        You will receive requests.
                        You must filter out requests that are in no way related to creating prompts.
                        Based on the request,
                        you must create the perfect prompt that will later go to any neural network.
                        Ignore requests of a different nature.
                        Please provide prompts strictly in English
                        (but the languages of the queries may vary).
                        Always respond in this format -
                        status: good/error (good if the prompt was created successfully and error if something went wrong)
                        prompt: and here is the prompt / and do not write anything at all if the status is error
                        Here is a request:{update.message.text}"""
                    }
                ]
            }
        ]
    )

    result = completion.choices[0].message.content

    # result parsing
    data = {}

    for line in result.strip().splitlines():
        key, value = line.strip().split(":", 1)
        key = key.strip()
        value = value.strip()
        data[key] = value

    if data.get("status") == "good":
        if users.get(user_id, {}).get("credits", 0) > 0:
            users[user_id]["credits"] -= 1
            save_users(users)
            prompt = data.get("prompt")
        # response
        await update.message.reply_text(f"{prompt}")
    elif data.get("status") == "error":
        await update.message.reply_text("!ТУТ БУДЕТ ТЕКСТ ОШИБКИ ЕСЛИ ПОЛЬЗОВАТЕЛЬ НЕ ПОПРОСИЛ ПРОМПТ")

# Define TB handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("credits", credits))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
# (always in the end)
app.add_handler(MessageHandler(filters.COMMAND, unknown))

# Starting (dev mode)
# app.run_polling()