from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests

def get_download_links(device_code):
    device_code = device_code.lower()
    
    json_url = f"https://raw.githubusercontent.com/AlphaDroid-devices/OTA/alpha-15.2/{device_code}.json"
    changelog_url = f"https://github.com/AlphaDroid-devices/OTA/blob/alpha-15.2/changelog_{device_code}.txt"

    try:
        response = requests.get(json_url)
        if response.status_code != 200:
            return f"❌ Device with codename {device_code} not found, make sure you are typing the correct codename.", None

        data = response.json()
        roms = data.get("response", [])

        if not roms:
            return "❌ No builds found for this device.", None

        maintainer = roms[0].get("maintainer", "Unknown")
        version = roms[0].get("version", "Unknown")
        telegram = None
        keyboard = []

        try:
            major_version = float(version.split(".")[0])
        except ValueError:
            major_version = 0

        status_icon = "🟢" if major_version >= 2 else "🔴"
        status_text = "Active" if major_version >= 2 else "Inactive"

        build_types = set()
        for rom in roms:
            if "buildvariant" in rom:
                build_types.add(rom["buildvariant"].capitalize()) 
            else:
                buildtype = rom.get("buildtype", "Unknown").lower()
                if "microg" in buildtype:
                    build_types.add("MicroG")
                elif "gapps" in buildtype:
                    build_types.add("GApps")
                else:
                    build_types.add("Vanilla")

        build_types_str = ", ".join(build_types)

        message = (
            f"✅ *Latest AlphaDroid build for {device_code}:*\n"
            f"📱 AlphaDroid Version: *{version}*\n"
            f"{status_icon} Status: *{status_text}*\n"
            f"🛠 Build Type: *{build_types_str}*\n"
            f"🧑‍💻 Maintainer: *{maintainer}*\n\n"
        )

        for rom in roms:
            if "buildvariant" in rom:
                variant_name = rom["buildvariant"].capitalize()
            else:
                buildtype = rom.get("buildtype", "Unknown").lower()
                if "microg" in buildtype:
                    variant_name = "MicroG"
                elif "gapps" in buildtype:
                    variant_name = "GApps"
                else:
                    variant_name = "Vanilla"

            download = rom.get("download", "No link")
            keyboard.append([InlineKeyboardButton(f"⬇ Download {variant_name}", url=download)])

            if not telegram and rom.get("telegram") and rom.get("telegram").startswith("https://t.me/"):
                telegram = rom.get("telegram")

        keyboard.append([InlineKeyboardButton("📃 Changelog", url=changelog_url)])

        if telegram:
            keyboard.append([InlineKeyboardButton("❗ Telegram", url=telegram)])

        reply_markup = InlineKeyboardMarkup(keyboard)
        return message, reply_markup
    except Exception as e:
        return f"❌ An error occurred: {e}", None

async def alpha(update: Update, context: CallbackContext) -> None:
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("⚠ Please provide a device code.\nExample: /alpha sunny", parse_mode="Markdown")
        return
    device_code = args[1]
    result, reply_markup = get_download_links(device_code)
    await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=reply_markup)
