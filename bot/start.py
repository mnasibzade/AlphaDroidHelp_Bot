import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import safe_reply

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in start command")
        return
    
    logger.info(f"User {update.effective_user.id} started the bot")
    
    welcome_message = (
        "👋 *Welcome to AlphaDroid Help Bot!*\n\n"
        "I'm here to help you with AlphaDroid ROM information and downloads.\n\n"
        "Use /help to see all available commands, or try these quick actions:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 Supported Devices", callback_data="devices")],
        [InlineKeyboardButton("📋 Help & Commands", callback_data="help")],
        [InlineKeyboardButton("🔗 Source Code", callback_data="source")]
    ]
    
    await safe_reply(
        update,
        welcome_message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
