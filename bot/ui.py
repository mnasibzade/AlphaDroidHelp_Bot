import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply

logger = logging.getLogger(__name__)


async def ui(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in ui command")
        return
    
    logger.info(f"User {update.effective_user.id} requested UI screenshots")
    
    keyboard = [
        [InlineKeyboardButton("UI references from 4.X (Latest)", url="https://t.me/alphadroid_releases/542")],
        [InlineKeyboardButton("3.X", url="https://t.me/alphadroid_releases/478")],
        [
            InlineKeyboardButton("2.X", url="https://t.me/alphadroid_releases/363"),
            InlineKeyboardButton("1.X", url="https://t.me/alphadroid_releases/154")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        "I think you are very curious about AlphaDroid!\n"
        "You can see the screenshots of the versions by clicking the buttons below.",
        reply_markup=reply_markup
    )
