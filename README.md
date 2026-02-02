# Commands
0. Environment creating
```bash
python -m venv venv
```
1. Start server
```bash
uvicorn server.main:server --reload
```
2. Start bot (by pooling)
```bash
python bot/bot.py
```
3. Preservation of requirements
```bash
pip freeze > requirements.txt
```
4. Webhook + Telegram Initialisation
- (Render)
```bash
curl -F "url=https://ai-prompt-generator-telegram-bot-server.onrender.com/tg-webhook" https://api.telegram.org/bot(bot_token)/setWebhook
```
- (Ngrok)
```bash
curl -F "url=(ngrok_url)/tg-webhook" https://api.telegram.org/bot(bot_token)/setWebhook
```
5. List of bot's comands
- start - Getting started
- help - Help with usage
- credits - Number of generations
- buy - Buy generation ❤️
- terms - Privacy Policy and Refund Policy

6. Dependencies install
```bash
pip install -r requirements.txt
```
