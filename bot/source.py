from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext


async def source(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Source code of AlphaDroid", url="https://github.com/alphadroid-project")],
        [InlineKeyboardButton("Source of OFFICIAL devices", url="https://github.com/AlphaDroid-devices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Here is the AlphaDroid Source Code!', reply_markup=reply_markup)
