from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def devices(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("List of OFFICIAL devices", url="https://alphadroid.org/#devices")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('You can find out whether your device is officially supported by us by clicking the button below.', reply_markup=reply_markup)
