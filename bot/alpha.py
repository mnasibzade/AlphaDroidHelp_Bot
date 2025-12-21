import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def get_download_links(device_code):
    device_code = device_code.lower().strip()
    
    json_url = f"https://raw.githubusercontent.com/AlphaDroid-devices/OTA/alpha-16.1/{device_code}.json"
    changelog_url = f"https://github.com/AlphaDroid-devices/OTA/blob/alpha-16.1/changelog_{device_code}.txt"

    try:
        response = requests.get(json_url, timeout=10)
        
        if response.status_code == 404:
            return f"❌ Device with codename *{device_code}* was not found. Please check the spelling.", None

        response.raise_for_status()
        data = response.json()
        roms = data.get("response", [])

        if not roms:
            return "❌ No builds found for this device.", None

        first_entry = roms[0]
        maintainer = first_entry.get("maintainer", "Unknown")
        version = first_entry.get("version", "Unknown")
        
        try:
            major_version = float(version.split(".")[0])
            status_icon = "🟢" if major_version >= 2 else "🔴"
            status_text = "Active" if major_version >= 2 else "Inactive"
        except (ValueError, IndexError):
            status_icon, status_text = "⚪", "Unknown"

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
                keyboard.append([InlineKeyboardButton(f"⬇️ Download {variant}", url=download_url)])
            
            if not telegram_link and rom.get("telegram"):
                telegram_link = rom.get("telegram")

        bottom_row = [InlineKeyboardButton("📃 Changelog", url=changelog_url)]
        if telegram_link:
            bottom_row.append(InlineKeyboardButton("❗ Telegram", url=telegram_link))
        
        keyboard.append(bottom_row)

        return message, InlineKeyboardMarkup(keyboard)

    except requests.exceptions.Timeout:
        return "⚠️ The server is taking too long to respond. Please try again later.", None
    except Exception as e:
        return f"❌ An unexpected error occurred: {str(e)}", None

async def alpha(update: Update, context: CallbackContext) -> None:
    args = update.message.text.split()
    
    if len(args) < 2:
        await update.message.reply_text(
            "⚠️ Please provide a device code.\nExample: `/alpha sunny`", 
            parse_mode="Markdown"
        )
        return

    device_code = args[1]
    result_text, reply_markup = get_download_links(device_code)
    
    await update.message.reply_text(
        result_text, 
        parse_mode="Markdown", 
        disable_web_page_preview=True, 
        reply_markup=reply_markup
    )
