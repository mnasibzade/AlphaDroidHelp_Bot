import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import asyncio

def read_token():
    try:
        with open('token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Token file (token.txt) not found.")
        return None

TOKEN = read_token()

if not TOKEN:
    print("Bot token is missing. Please make sure the token.txt file exists.")
    exit()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Type /help to see my commands!')

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

async def contribute(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Donate to us", url="https://www.paypal.com/donate/?hosted_button_id=UKKSXJYZDMH58")],
        [InlineKeyboardButton("Help us with translation!", url="https://crowdin.com/project/alphadroid_alphasettings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('We are an open-source project and we are open to your contributions', reply_markup=reply_markup)

async def ui(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("UI references from 3.X", url="https://t.me/alphadroid_chat/63893")],
        [InlineKeyboardButton("2.X", url="https://t.me/alphadroid_releases/363"), InlineKeyboardButton("1.X", url="https://t.me/alphadroid_releases/154")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "I think you are very curious about AlphaDroid!\n"
        "You can see the screenshots of the required version by clicking the buttons below.",
        reply_markup=reply_markup
    )

async def releases(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("AlphaDroid Releases Channel", url="https://t.me/alphadroid_releases")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Stay informed about AlphaDroid releases!', reply_markup=reply_markup)

async def apply(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Apply Now", url="https://github.com/AlphaDroid-devices/official_devices/blob/main/README.md")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hmm do you want to maintain your device officially?\nYou can learn the conditions and how to apply from the link below', reply_markup=reply_markup)

async def devices_list(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("List of OFFICIAL devices", url="https://github.com/AlphaDroid-devices/official_devices/blob/main/devices.md")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('You can find out whether your device is officially supported by us by clicking the button below.', reply_markup=reply_markup)

async def source(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Source code of AlphaDroid", url="https://github.com/alphadroid-project")],
        [InlineKeyboardButton("Source of OFFICIAL devices", url="https://github.com/AlphaDroid-devices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Here is the AlphaDroid Source Code!', reply_markup=reply_markup)

def get_download_links(device_code):
    device_code = device_code.lower()
    
    json_url = f"https://raw.githubusercontent.com/AlphaDroid-devices/OTA/alpha-15.1/{device_code}.json"
    changelog_url = f"https://github.com/AlphaDroid-devices/OTA/blob/alpha-15.1/changelog_{device_code}.txt"

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

def main():
    app = Application.builder().token(TOKEN).job_queue(None).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ui", ui))
    app.add_handler(CommandHandler("releases", releases))
    app.add_handler(CommandHandler("source", source))
    app.add_handler(CommandHandler("contribute", contribute))
    app.add_handler(CommandHandler("apply", apply))
    app.add_handler(CommandHandler("devices", devices_list))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("alpha", alpha))

    app.run_polling()

if __name__ == '__main__':
    main()
