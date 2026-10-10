# 🤖 Discord Smart DM Auto-Responder

<p align="center">
  <b>Context-aware Discord DM Auto-Responder with Activity Detection, Anti-Spam Cooldown & 24/7 Cloud Support</b>
</p>

<p align="center">
  <a href="https://github.com/storm-dev-arch/discord-smart-autoresponder/releases"><img src="https://img.shields.io/github/v/release/storm-dev-arch/discord-smart-autoresponder?color=blue&style=for-the-badge" alt="Release"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Cloud-Render.com%2024%2F7-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render.com">
  <img src="https://img.shields.io/badge/Library-discord.py--self-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py-self">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## ✨ Features

- **🧠 Activity-Aware Dynamic Replies**:
  - Automatically checks what you are currently doing (Spotify playback, Google Antigravity, Counter-Strike 2, Dota 2, Roblox, streaming, or watching).
  - Generates realistic, natural replies based on current context (e.g., *"Привет. Я сейчас в игре Counter-Strike 2. Как освобожусь, сразу отвечу."*).
  - Clean text without emojis or AI-slop stickers.

- **⏱️ Anti-Spam Smart Cooldown**:
  - Remembers who was messaged and enforces a per-user cooldown (default: 5 minutes / 300s).
  - Subsequent messages from the same user are ignored until the cooldown expires.

- **🧪 Built-in Self-Testing (`!test`)**:
  - Send `!test` to any chat or DM from your own account.
  - The bot immediately generates and replies with your active status so you can verify it anytime without needing a second account or friend.

- **☁️ 24/7 Cloud Ready (Render.com / Docker / VPS)**:
  - Built-in lightweight HTTP health check server on `$PORT` to comply with Render.com Free Web Service requirements.
  - Can run both locally in the background on Windows or 24/7 on cloud hosting.

---

## 🛠️ Project Structure

```
discord-smart-autoresponder/
├── autoresponder.py      # Main bot client & activity analyzer
├── config.example.json   # Template configuration file
├── requirements.txt      # Python dependencies
├── Procfile              # Render / Heroku process declaration
├── render.yaml           # One-click Render.com deployment blueprint
├── run_silent.vbs        # Silent background launcher for Windows
├── start.bat / stop.bat  # Windows control scripts
└── .gitignore            # Keeps your tokens and secrets secure
```

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.10+
- A Discord User Token

### 2. Installation
```bash
git clone https://github.com/storm-dev-arch/discord-smart-autoresponder.git
cd discord-smart-autoresponder
pip install -r requirements.txt
```

### 3. Local Configuration
1. Copy `config.example.json` to `config.json`:
   ```bash
   cp config.example.json config.json
   ```
2. Insert your Discord Token:
   ```json
   {
       "token": "YOUR_DISCORD_TOKEN",
       "cooldown_seconds": 300,
       "only_dms": true,
       "ignored_user_ids": []
   }
   ```
3. Run:
   ```bash
   python autoresponder.py
   ```

---

## ☁️ 24/7 Cloud Deployment (Render.com)

1. Fork or push this repository to your GitHub.
2. In [Render Dashboard](https://dashboard.render.com), click **New +** -> **Web Service**.
3. Select this repository.
4. Set:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python autoresponder.py`
5. In **Environment Variables**, add:
   - `DISCORD_TOKEN`: `your_discord_token`
   - `RENDER`: `true`
6. Deploy! The built-in HTTP server will automatically satisfy Render's health checks.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
