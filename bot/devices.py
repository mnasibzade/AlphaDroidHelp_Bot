import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply
import config

logger = logging.getLogger(__name__)


async def devices(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in devices command")
        return
    
    logger.info(f"User {update.effective_user.id} requested devices list")
    
    keyboard = [
        [InlineKeyboardButton("List of OFFICIAL devices", url=config.ALPHADROID_WEBSITE)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await safe_reply(
        update,
        'You can find out whether your device is officially supported by us by clicking the button below.',
        reply_markup=reply_markup
    )
