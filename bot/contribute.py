import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply
import config

logger = logging.getLogger(__name__)


async def contribute(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in contribute command")
        return
    
    logger.info(f"User {update.effective_user.id} requested contribution info")
    
    keyboard = [
        [InlineKeyboardButton("Donate to us", url=config.DONATION_LINK)],
        [InlineKeyboardButton("Help us with translation!", url=config.TRANSLATION_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        'We are an open-source project and we are open to your contributions',
        reply_markup=reply_markup
    )
