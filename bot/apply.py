import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply
import config

logger = logging.getLogger(__name__)


async def apply(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in apply command")
        return
    
    logger.info(f"User {update.effective_user.id} requested maintainer application info")
    
    keyboard = [
        [InlineKeyboardButton("Apply Now", url=config.MAINTAINER_APPLICATION)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        'Hmm do you want to maintain your device officially?\nYou can learn the conditions and how to apply from the link below',
        reply_markup=reply_markup
    )
