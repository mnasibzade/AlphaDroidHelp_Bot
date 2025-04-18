import time
from telegram import Update
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    start_time = time.time()

    message = await update.message.reply_text('Welcome! Type /help to see my commands!')

    end_time = time.time()
    ping = int((end_time - start_time) * 1000)  # ping in ms

    await message.edit_text(
        f"👋 Welcome! Type /help to see my commands!\n"
        f"📡 Ping: `{ping}ms`\n\n"
        f"If you have any issues, feel free to [open an issue on GitHub](https://github.com/mnasibzade/AlphaDroidHelp_Bot/issues).",
        parse_mode="Markdown"
    )
