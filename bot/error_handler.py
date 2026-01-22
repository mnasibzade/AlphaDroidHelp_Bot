"""
Global error handler for AlphaDroid Telegram Bot
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import (
    TelegramError,
    NetworkError,
    BadRequest,
    TimedOut,
    Conflict
)

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: CallbackContext) -> None:
    """
    Global error handler for the bot.
    
    Logs errors and sends user-friendly messages when possible.
    
    Args:
        update: The update that caused the error
        context: The context object containing error information
    """
    # Log the error
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    
    # Don't try to send messages if update is not a proper Update object
    if not isinstance(update, Update):
        return
    
    # Prepare user message based on error type
    user_message = None
    
    if isinstance(context.error, BadRequest):
        if "invalid" in str(context.error).lower() and "url" in str(context.error).lower():
            user_message = (
                "❌ An error occurred with a URL in the response. "
                "This has been logged and will be fixed soon."
            )
            logger.critical(f"Invalid URL error: {context.error}")
        else:
            user_message = "❌ Invalid request. Please check your input and try again."
    
    elif isinstance(context.error, TimedOut):
        user_message = (
            "⏱️ The request timed out. The server might be slow or unavailable.\n"
            "Please try again in a few moments."
        )
    
    elif isinstance(context.error, NetworkError):
        user_message = (
            "🌐 Network error occurred. This might be a temporary issue.\n"
            "Please try again later."
        )
    
    elif isinstance(context.error, Conflict):
        logger.warning("Conflict error - multiple bot instances might be running")
        # Don't send message to user for this error
        return
    
    else:
        user_message = (
            "❌ An unexpected error occurred. The issue has been logged.\n"
            "Please try again later."
        )
    
    # Try to send error message to user
    if user_message:
        try:
            if update.message:
                await update.message.reply_text(user_message)
            elif update.callback_query:
                await update.callback_query.message.reply_text(user_message)
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")
