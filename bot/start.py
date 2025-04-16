from telegram import Update
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Type /help to see my commands!')
