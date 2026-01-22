import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply
import config

logger = logging.getLogger(__name__)


async def source(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in source command")
        return
    
    logger.info(f"User {update.effective_user.id} requested source code links")
    
    keyboard = [
        [InlineKeyboardButton("AlphaDroid Source Code", url=config.ALPHADROID_SOURCE)],
        [InlineKeyboardButton("Official Devices Resources", url=config.ALPHADROID_DEVICES_REPO)],
        [InlineKeyboardButton("Bot Source Code", url=config.BOT_SOURCE)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        'Looking for the source? Here you go! 👇',
        reply_markup=reply_markup
    )
