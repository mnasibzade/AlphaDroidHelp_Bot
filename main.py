import sys
import os
import logging
from telegram.ext import Application, CommandHandler
from bot.start import start
from bot.help import help
from bot.alpha import alpha
from bot.ui import ui
from bot.releases import releases
from bot.source import source
from bot.contribute import contribute
from bot.apply import apply
from bot.devices import devices
from bot.error_handler import error_handler
import config


def setup_logging():
    logging.basicConfig(
        format=config.LOG_FORMAT,
        level=getattr(logging, config.LOG_LEVEL),
        handlers=[
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set httpx and httpcore to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")
    return logger


def read_token():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        token_path = os.path.join(base_dir, config.BOT_TOKEN_FILE)
        
        with open(token_path, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            
        if not token:
            print(f"Error: {config.BOT_TOKEN_FILE} is empty.", file=sys.stderr)
            return None
            
        return token
        
    except FileNotFoundError:
        print(f"Error: {config.BOT_TOKEN_FILE} not found in {os.path.dirname(os.path.abspath(__file__))}", file=sys.stderr)
        print(f"Please create {config.BOT_TOKEN_FILE} and add your bot token.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading token file: {e}", file=sys.stderr)
        return None


def main():
    # Setup logging first
    logger = setup_logging()
    
    # Read bot token
    logger.info("Reading bot token...")
    TOKEN = read_token()
    
    if not TOKEN:
        logger.error("Bot token is missing. Exiting.")
        sys.exit(1)
    
    logger.info("Bot token loaded successfully")
    
    # Build application
    logger.info("Building application...")
    app = Application.builder().token(TOKEN).build()
    
    # Register error handler
    app.add_error_handler(error_handler)
    logger.info("Error handler registered")
    
    # Register command handlers
    logger.info("Registering command handlers...")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("alpha", alpha))
    app.add_handler(CommandHandler("ui", ui))
    app.add_handler(CommandHandler("releases", releases))
    app.add_handler(CommandHandler("source", source))
    app.add_handler(CommandHandler("contribute", contribute))
    app.add_handler(CommandHandler("apply", apply))
    app.add_handler(CommandHandler("devices", devices))
    
    logger.info("All handlers registered successfully")
    logger.info("Starting bot...")
    
    # Run the bot
    try:
        app.run_polling(allowed_updates=["message", "callback_query"])
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
