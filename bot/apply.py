from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def apply(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Apply Now", url="https://github.com/AlphaDroid-devices/official_devices/blob/main/README.md")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hmm do you want to maintain your device officially?\nYou can learn the conditions and how to apply from the link below', reply_markup=reply_markup)
