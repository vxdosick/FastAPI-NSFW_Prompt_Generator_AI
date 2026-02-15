# NSFW_Prompt_Generator_AI
### Bot name: @nsfw_prompt_generator_bot

### Functionality / Features
NSFW Prompt Generator AI is an AI-powered assistant designed to generate detailed prompts for adult-oriented image generation models. Key features include:

* AI-powered Prompt Generation – create structured, high-detail prompts based on user descriptions.
* Model Optimization – prompts are optimized for Stable Diffusion, SDXL, Pony, Flux, Autismix, and other compatible models.
* Unrestricted Creative Input – supports explicit, uncensored prompt construction according to user requests.
* Ready-to-Use Output – generates copy-ready prompts for seamless integration into image generation workflows.
* Fast & Lightweight – simple interface without complex dashboards or unnecessary steps.
* Free Trial Access – new users receive a limited number of free generations to explore functionality.

This bot streamlines the process of creating high-quality adult prompts, making prompt engineering faster, more accessible, and more efficient for AI image generation platforms.

### Information about the bot
1. An AI bot for generating advanced prompts for various generative AI models.
2. The DEV version of the project uses [Ngrok](https://ngrok.com).
3. The MVP version of the project uses [Render](https://render.com) as Cloud.

### List of bot's comands
1. /start - Getting started
2. /help - Help with usage
3. /credits - Number of generations
4. /buy - Buy mgeneration ❤️
5. /terms - Privacy Policy and Refund Policy

### Main stack
- Python 3.12.12
- Telegram Bot API (python-telegram-bot)
- FastAPI — REST API layer
- SQLite — lightweight database
- SQLAlchemy 2.0 — ORM
- OpenRouter API — AI integration
- Uvicorn — ASGI server
- Render - deployment (MVP)
- Ngrok - local tunneling for webhook testing (DEV)
- Stripe - Payment system

### Useful commands
0. Environment creating
```bash
python -m venv venv
```
1. Create .env file in root direction and write inside:
```bash
BOT_TOKEN=...
SERVER_URL=...
STRIPE_LIVE_SECRET_KEY=...
OPENAI_API_KEY=...
STRIPE_LIVE_WEBHOOK_SECRET=...
```
2. Start server
```bash
uvicorn server.main:server --reload
```
3. Ngrok starting
```bash
ngrok http 8000
```
4. Start bot (by pooling)
```bash
python bot/bot.py
```
5. Preservation of requirements
```bash
pip freeze > requirements.txt
```
6. Webhook - Telegram Initialisation
```bash
curl -F "url=(ngrok_url or render_url)/tg-webhook" https://api.telegram.org/bot(bot_token)/setWebhook
```
7. Dependencies install
```bash
pip install -r requirements.txt
```
