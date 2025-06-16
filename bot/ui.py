from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def ui(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("UI references from 3.X", url="https://t.me/alphadroid_releases/478")],
        [InlineKeyboardButton("2.X", url="https://t.me/alphadroid_releases/363"), InlineKeyboardButton("1.X", url="https://t.me/alphadroid_releases/154")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "I think you are very curious about AlphaDroid!\n"
        "You can see the screenshots of the required version by clicking the buttons below.",
        reply_markup=reply_markup
    )
