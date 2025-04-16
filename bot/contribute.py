from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def contribute(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Donate to us", url="https://www.paypal.com/donate/?hosted_button_id=UKKSXJYZDMH58")],
        [InlineKeyboardButton("Help us with translation!", url="https://crowdin.com/project/alphadroid_alphasettings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('We are an open-source project and we are open to your contributions', reply_markup=reply_markup)
