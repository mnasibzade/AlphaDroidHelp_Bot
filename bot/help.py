import logging
from telegram import Update
from telegram.ext import CallbackContext
from bot.utils import safe_reply

logger = logging.getLogger(__name__)


async def help(update: Update, context: CallbackContext) -> None:
    if not update.message:
        logger.warning("Received update without message in help command")
        return
    
    logger.info(f"User {update.effective_user.id} requested help")
    
    help_text = (
        "Hello, I am a bot written for AlphaDroid. My mission is to provide support to AlphaDroid users and make my team's job easier!\n\n"
        "Here's a list of my commands (sorted alphabetically):\n"
        "/alpha <device_codename> — Get the download link for your device\n"
        "/apply — Apply for official maintainership\n"
        "/contribute — Learn how to support or contribute to the project\n"
        "/devices — See the list of supported devices\n"
        "/releases — Stay up to date with AlphaDroid releases\n"
        "/source — View AlphaDroid's and Bot's source code\n"
        "/start — Make sure the bot is alive\n"
        "/ui — Get screenshots of UI from previous versions"
    )
    
    await safe_reply(update, help_text)
