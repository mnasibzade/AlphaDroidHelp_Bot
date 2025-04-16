from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def releases(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("AlphaDroid Releases Channel", url="https://t.me/alphadroid_releases")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Stay informed about AlphaDroid releases!', reply_markup=reply_markup)
