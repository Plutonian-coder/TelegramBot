TelegramBot
===========

A simple Telegram bot that uses Google Gemini + python-telegram-bot.

Start command (for Render)
-------------------------
Render runs the command below to start your app on deploy. This bot is a background worker (it doesn't serve HTTP), so use a Background Worker service on Render and set the start command to:

```
python bot.py
```

If you are using a Procfile, the worker entry is provided in `Procfile`:

```
worker: python bot.py
```

Environment variables
---------------------
Set the following in Render (or in your environment):

- TELEGRAM_BOT_TOKEN — your bot token
- GOOGLE_API_KEY — your Google (Gemini) API key

Deploy notes
------------
- This repo includes `requirements.txt`. Render will install dependencies automatically.
- Use a Background Worker service (not a Web Service) since this bot listens to Telegram updates.
- If you prefer a Web Service, you'd need to run a web server and webhook handling (not included).

Local run
---------
Start the bot locally with:

```cmd
python bot.py
```

Security
--------
Do not commit API keys. Use Render secrets or environment variables to store tokens.
