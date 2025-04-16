import json
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
from bot.start import start
from bot.help import help
from bot.alpha import alpha
from bot.ui import ui
from bot.releases import releases
from bot.source import source
from bot.contribute import contribute
from bot.apply import apply
from bot.devices import devices

def read_token():
    try:
        with open('token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Token file (token.txt) not found.")
        return None

TOKEN = read_token()

if not TOKEN:
    print("Bot token is missing. Please make sure the token.txt file exists.")
    exit()

def main():
    app = Application.builder().token(TOKEN).job_queue(None).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("alpha", alpha))
    app.add_handler(CommandHandler("ui", ui))
    app.add_handler(CommandHandler("releases", releases))
    app.add_handler(CommandHandler("source", source))
    app.add_handler(CommandHandler("contribute", contribute))
    app.add_handler(CommandHandler("apply", apply))
    app.add_handler(CommandHandler("devices", devices))

    app.run_polling()

if __name__ == '__main__':
    main()
