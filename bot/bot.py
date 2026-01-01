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
SERVER_NGROK = os.getenv('SERVER_NGROK')

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

    if users[user_id]["credits"] == 0:
        await update.message.reply_text(
            f"Hey there! 👋😈\n\n"
            f"Welcome to your Uncensored NSFW Prompt Generator AI -\n"
            f"the ultimate AI sidekick that turns your wildest fantasies into\n"                      
            f"ultra-detailed, fully uncensored prompts 🔥\n\n"            
            f"Just describe your spicy idea (the dirtier, the better 😉),\n"                        
            f"and I’ll instantly craft a powerful prompt perfectly tuned for\n"                         
            f"Stable Diffusion, Pony, Flux, SDXL, or any uncensored model.\n\n"                        
            f"No limits. No filters. Pure creative freedom 💦\n\n"
            f"Generations used up 😇 No worries - you can more generations!\n"
            f"Type /buy for details 🔥")
    else:
        await update.message.reply_text(
            f"Hey there! 👋😈\n\n"
            f"Welcome to your Uncensored NSFW Prompt Generator AI -\n"
            f"the ultimate AI sidekick that turns your wildest fantasies into\n"                      
            f"ultra-detailed, fully uncensored prompts 🔥\n\n"            
            f"Just describe your spicy idea (the dirtier, the better 😉),\n"                        
            f"and I’ll instantly craft a powerful prompt perfectly tuned for\n"                         
            f"Stable Diffusion, Pony, Flux, SDXL, or any uncensored model.\n\n"                        
            f"No limits. No filters. Pure creative freedom 💦\n\n"
            f"New users get 5 free generations as a welcome gift -"
            f"let’s get started right now!🎁\n\n"
            f"Remaining generations: {users[user_id]["credits"]}💎")

async def help(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    await update.message.reply_text(
            f"Need help? Here's everything you need to know 😏🔥\n\n"
            f"🔹 How it works:\n"
            f"Just send me any description of your fantasy — characters, scene, pose, style, uncensored... anything! "
            f"The naughtier your idea, the better the prompt I'll create 😉\n\n"
            f"🔹 What I do:\n"
            f"- Generate highly detailed, fully uncensored prompts\n"
            f"- Optimized for Stable Diffusion, Pony, Flux, SDXL & other uncensored models\n"
            f"- Add quality boosters, weights, lighting, styles, negative prompts — everything for stunning results 🎨\n\n"
            f"🔹 Commands:\n"
            f"/start — Show welcome message & check remaining generations\n"
            f"/help — This help menu\n"
            f"/buy — Buy more generations\n"
            f"/credits — Check how many free generations you have left\n\n"
            f"🔹 Tip:\n"
            f"Be as specific (or as wild) as you want — I handle everything without judgment 💦\n\n"
            f"Ready to create something spicy? Just type your idea now! 😈")

async def credits(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    user_id = str(update.effective_user.id)
    users = load_users()

    credits = users.get(user_id, {}).get("credits", 0)

    await update.message.reply_text(
            f"Your generations status 💎😏\n\n"
            f"Free generations left: {credits} 🎁\n\n"
            f"5 free generations for new users🎁\n"
            f"Out of free ones? Go unlimited with /buy 🔥\n\n"
            f"Ready for more? Just send your fantasy! 💦")

async def buy(update, context):
    user_id = str(update.effective_user.id)

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVER_URL}/create-checkout-session/{user_id}")
        data = r.json()
        await update.message.reply_text(
            f"Ready to unlock more spicy generations? 😏🔥\n\n"
            f"One simple purchase — no subscriptions, no hidden fees, no monthly traps.\n"
            f"Everything is transparent and honest 💎\n\n"
            f"For just €1.99 you get 10 full generations!\n"
            f"That's less than a coffee ☕ — but way hotter and more satisfying 😉\n\n"
            f"Pay once → instantly get your 10 generations added.\n"
            f"As simple as that!\n\n"
            f"<a href='{data['url']}'>🛒 Grab 10 generations for €1.99 now!</a>\n\n"
            f"Let's keep the creativity flowing! 💦")

async def unknown(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    await update.message.reply_text(
            f"Oops! 😅 That command doesn't exist yet.\n\n"
            f"Try one of these:\n"
            f"/start — Welcome message & generations info\n"
            f"/help — How to use me\n"
            f"/credits — Check free generations left\n"
            f"/buy — Get more generations (€1.99 for 10)\n\n"
            f"Or just describe your fantasy — I'll create a hot prompt right away! 🔥💦")

# Requests (text in telegram)
async def echo(update, context):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    
    user_id = str(update.effective_user.id)
    users = load_users()
    
    if is_rate_limited(user_id):
        await update.message.reply_text(
            f"Whoa there, slow down a bit! 😏🔥\n\n"
            f"You're sending requests too fast — let's take a quick breath.\n"
            f"Wait just 5-10 seconds and try again 😉\n\n"
            f"I want to give you the best prompts, not rush them! 💦")
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
        await update.message.reply_text(
            f"Oops! 😅 I couldn't process that request.\n\n"
            f"It looks like you might have asked for something else entirely (not a prompt request), "
            f"or it involved minors/extreme illegal content — that's a no-go.\n\n"
            f"Please describe a fantasy for adult characters (18+ only) and keep it focused on a hot NSFW prompt 😉\n\n"
            f"Try again with something spicy and clear! 💦")

# Define TB handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("credits", credits))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
# (always in the end)
app.add_handler(MessageHandler(filters.COMMAND, unknown))