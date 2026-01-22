"""
Configuration file for AlphaDroid Telegram Bot
"""
import os

# Bot Configuration
BOT_TOKEN_FILE = "token.txt"

# API URLs
ALPHADROID_OTA_BASE_URL = "https://raw.githubusercontent.com/AlphaDroid-devices/OTA/alpha-16.1"
ALPHADROID_CHANGELOG_BASE_URL = "https://github.com/AlphaDroid-devices/OTA/blob/alpha-16.1"

# Timeout Settings (in seconds)
API_REQUEST_TIMEOUT = 10
TELEGRAM_TIMEOUT = 30

# Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_MESSAGES = 5  # messages per window
RATE_LIMIT_WINDOW = 60   # seconds

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "bot.log"

# Version Status
ACTIVE_VERSION_THRESHOLD = 2.0  # Versions >= 2.0 are considered active

# External Links
ALPHADROID_WEBSITE = "https://alphadroid.org/#devices"
ALPHADROID_SOURCE = "https://github.com/alphadroid-project"
ALPHADROID_DEVICES_REPO = "https://github.com/AlphaDroid-devices"
ALPHADROID_RELEASES_CHANNEL = "https://t.me/alphadroid_releases"
BOT_SOURCE = "https://github.com/mnasibzade/AlphaDroidHelp_Bot"
DONATION_LINK = "https://www.paypal.com/donate/?hosted_button_id=UKKSXJYZDMH58"
TRANSLATION_LINK = "https://crowdin.com/project/alphadroid_alphasettings"
MAINTAINER_APPLICATION = "https://github.com/AlphaDroid-devices/official_devices/blob/main/README.md"
