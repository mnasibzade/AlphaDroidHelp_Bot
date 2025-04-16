from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def source(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("AlphaDroid Source Code", url="https://github.com/alphadroid-project")],
        [InlineKeyboardButton("Official Devices Resources", url="https://github.com/AlphaDroid-devices")],
        [InlineKeyboardButton("Bot Source Code", url="https://github.com/mnasibzade/AlphaDroidHelp_Bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Looking for the source? Here you go! 👇', reply_markup=reply_markup)
