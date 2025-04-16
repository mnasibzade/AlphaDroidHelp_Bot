from telegram import Update
from telegram.ext import CallbackContext

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello, I am a bot written for AlphaDroid. My mission is to provide support to AlphaDroid users and make my team's job easier!\n"
        "Here's a list of my commands (sorted alphabetically):\n"
        "/alpha <device_codename> - Get the download link for your device\n"
        "/apply - Apply for maintainership!\n" 
        "/contribute - If you want to support us!\n"
        "/devices - Get the list of supported devices\n" 
        "/releases - Check AlphaDroid releases\n"
        "/source - Shows our source code\n"
        "/start - Check if I am alive\n"
        "/ui - Do you need screenshots? Use me!"
    )
