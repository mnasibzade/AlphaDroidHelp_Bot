import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils import sanitize_url, safe_reply, format_error_message, validate_device_code, get_status_info
import config

logger = logging.getLogger(__name__)


def get_download_links(device_code: str) -> tuple[str, InlineKeyboardMarkup | None]:
    device_code = device_code.lower().strip()
    
    # Validate device code format
    if not validate_device_code(device_code):
        logger.warning(f"Invalid device code format: {device_code}")
        return format_error_message('device_not_found'), None
    
    json_url = f"{config.ALPHADROID_OTA_BASE_URL}/{device_code}.json"
    changelog_url = f"{config.ALPHADROID_CHANGELOG_BASE_URL}/changelog_{device_code}.txt"

    try:
        logger.info(f"Fetching device info for: {device_code}")
        response = requests.get(json_url, timeout=config.API_REQUEST_TIMEOUT)
        
        if response.status_code == 404:
            logger.info(f"Device not found: {device_code}")
            return f"❌ Device with codename *{device_code}* was not found. Please check the spelling.", None

        response.raise_for_status()
        data = response.json()
        roms = data.get("response", [])

        if not roms:
            logger.warning(f"No builds found for device: {device_code}")
            return "❌ No builds found for this device.", None

        first_entry = roms[0]
        maintainer = first_entry.get("maintainer", "Unknown")
        version = first_entry.get("version", "Unknown")
        
        # Get status info using utility function
        status_icon, status_text = get_status_info(version)

        build_types = set()
        for rom in roms:
            variant = rom.get("buildvariant", rom.get("buildtype", "Vanilla")).capitalize()
            build_types.add(variant)

        message = (
            f"✅ *Latest AlphaDroid for {device_code}:*\n\n"
            f"📱 Version: *{version}*\n"
            f"{status_icon} Status: *{status_text}*\n"
            f"🛠 Build Types: *{', '.join(build_types)}*\n"
            f"🧑‍💻 Maintainer: *{maintainer}*\n"
        )

        keyboard = []
        telegram_link = None

        for rom in roms:
            variant = rom.get("buildvariant", rom.get("buildtype", "Build")).capitalize()
            download_url = rom.get("download")
            
            if download_url:
                # Sanitize download URL
                download_url = sanitize_url(download_url)
                if download_url:
                    keyboard.append([InlineKeyboardButton(f"⬇️ Download {variant}", url=download_url)])
                else:
                    logger.error(f"Invalid download URL for {device_code}: {rom.get('download')}")
            
            if not telegram_link and rom.get("telegram"):
                telegram_link = rom.get("telegram")

        bottom_row = [InlineKeyboardButton("📃 Changelog", url=changelog_url)]
        
        if telegram_link:
            # CRITICAL FIX: Sanitize Telegram URL to prevent double https://
            telegram_link = sanitize_url(telegram_link)
            if telegram_link:
                bottom_row.append(InlineKeyboardButton("❗ Telegram", url=telegram_link))
            else:
                logger.error(f"Invalid Telegram URL for {device_code}: {first_entry.get('telegram')}")
        
        keyboard.append(bottom_row)

        logger.info(f"Successfully fetched info for device: {device_code}")
        return message, InlineKeyboardMarkup(keyboard)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching device info for: {device_code}")
        return format_error_message('timeout'), None
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error for device {device_code}: {e}")
        return format_error_message('network_error'), None
    except ValueError as e:
        logger.error(f"JSON parsing error for device {device_code}: {e}")
        return format_error_message('api_error', "Invalid response from server"), None
    except Exception as e:
        logger.error(f"Unexpected error for device {device_code}: {e}", exc_info=True)
        return format_error_message('unknown', str(e)), None


async def alpha(update: Update, context: CallbackContext) -> None:
    # Check if update has message (prevent NoneType error)
    if not update.message:
        logger.warning("Received update without message in alpha command")
        return
    
    args = update.message.text.split()
    
    if len(args) < 2:
        await safe_reply(
            update,
            "⚠️ Please provide a device code.\nExample: `/alpha sunny`", 
            parse_mode="Markdown"
        )
        return

    device_code = args[1]
    logger.info(f"Processing /alpha command for device: {device_code}")
    
    result_text, reply_markup = get_download_links(device_code)
    
    await safe_reply(
        update,
        result_text, 
        parse_mode="Markdown", 
        disable_web_page_preview=True, 
        reply_markup=reply_markup
    )
