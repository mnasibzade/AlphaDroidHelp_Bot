import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply
import config

logger = logging.getLogger(__name__)


async def releases(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in releases command")
        return
    
    logger.info(f"User {update.effective_user.id} requested releases channel")
    
    keyboard = [
        [InlineKeyboardButton("AlphaDroid Releases Channel", url=config.ALPHADROID_RELEASES_CHANNEL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        'Stay informed about AlphaDroid releases!',
        reply_markup=reply_markup
    )
