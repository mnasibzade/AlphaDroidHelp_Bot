# AlphaDroidHelp_Bot

Hey there! This bot was created to help users in the [AlphaDroid](https://github.com/AlphaDroid-Project) Telegram community and make things easier for both users and team members. 🚀

---

## 🎯 Purpose

The main goal of this bot is to provide fast, simple, and clear support to AlphaDroid users.  
But that's not all — the reason I made this bot open to everyone is so that other **AOSP ROM communities** can benefit from it too. I hope it helps users easily find what they’re looking for, no matter which project they’re part of.

> If you’d like to add more features or improve something, **Pull Requests are more than welcome!** 🤝

---

Absolutely! Here's an updated and more detailed **"How to Use"** section for your README, including steps for setting up the bot token and running it properly:

---

## 💡 How to Use

Follow these steps to get the AlphaDroidHelp Bot up and running on your machine:

### 1. **Clone the Repository**
```bash
git clone https://github.com/mnasibzade/AlphaDroidHelp_Bot
cd AlphaDroidBot
```

### 2. **Install Dependencies**
Make sure you have Python installed. Then install required Python packages:
```bash
pip install -r requirements.txt
```

### 3. **Get a Telegram Bot Token**
- Talk to [@BotFather](https://t.me/BotFather) on Telegram.
- Use the `/newbot` command and follow the instructions to create your bot.
- Once created, BotFather will give you a **bot token** (e.g., `123456789:ABCdefGHIjkLMNOPqrsTUVwxyZ`).

### 4. **Save Your Token**
Create a file named `token.txt` in the root directory of the project:
```bash
touch token.txt
```
Then paste your token inside the file (only the token string, nothing else):
```
123456789:ABCdefGHIjkLMNOPqrsTUVwxyZ
```

### 5. **Run the Bot**
Now you're ready to start the bot:
```bash
python main.py
```
- To run the bot 24/7, you'll need to host it on a machine that stays online — like a VPS, cloud service, or your own server.
There are many platforms you can explore, such as Railway, Render, Replit, or traditional VPS providers like Hetzner or DigitalOcean. You’ll need a constantly running environment — feel free to research which option fits your needs best!

If everything is set up correctly, you’ll see the bot is running and waiting for commands.

---

## 🔧 Commands

Here's what the bot can do for you:

- `/alpha <device_codename>` — Get the download link for your device  
- `/apply` — Apply for official maintainership  
- `/contribute` — Learn how to support or contribute to the project  
- `/devices` — See the list of supported devices  
- `/releases` — Stay up to date with AlphaDroid releases  
- `/source` — View AlphaDroid’s source code  
- `/start` — Make sure the bot is alive  
- `/ui` — Get screenshots of UI from previous versions
