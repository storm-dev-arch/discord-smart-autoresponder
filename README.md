# 🤖 Discord Smart Auto-Responder & Telegram Bridge

<p align="center">
  <b>Context-aware Discord Auto-Responder with 2-Way Telegram Bridge, Activity Detection & 24/7 Cloud Support</b><br>
  <i>Двусторонний Telegram-мост для Discord с ответами свайпом из Telegram, автоответчиком и работой 24/7</i>
</p>

<p align="center">
  <a href="#russian">🇷🇺 Читать на русском</a> • <a href="#english">🇬🇧 English Readme</a>
</p>

<p align="center">
  <a href="https://github.com/storm-dev-arch/discord-smart-autoresponder/releases"><img src="https://img.shields.io/github/v/release/storm-dev-arch/discord-smart-autoresponder?color=blue&style=for-the-badge" alt="Release"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Bridge-Telegram%20%3C--%3E%20Discord-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Bridge">
  <img src="https://img.shields.io/badge/Cloud-Render.com%2024%2F7-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render.com">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

<a name="russian"></a>
## 🇷🇺 Документация на русском

### ✨ Главные возможности

#### 📱 Двусторонний Telegram-мост (Telegram <-> Discord Bridge):
- **Входящие в Telegram**: все личные сообщения из Discord мгновенно прилетают тебе в Telegram-бота с именем отправителя, тегом, ID и текстом/вложениями.
- **Ответ свайпом (Swipe-to-Reply)**: чтобы ответить человеку в Discord, тебе не нужно открывать приложение Discord — **просто свайпни сообщение в Telegram и напиши ответ**. Бот сам отправит его в нужный чат Discord от твоего имени!
- **Управление через команды в Telegram**:
  - `/status` — статус Discord-аккаунта, пинг, текущая активность и состояние автоответчика.
  - `/toggle` — включить / выключить автоответчик прямо из Telegram (удобно, когда сам активно переписываешься через Telegram-мост).
  - `/send <user_id> <текст>` — инициировать диалог в ЛС с любым пользователем Discord по его ID.
  - `/help` — справка по командам.

#### 🧠 Умный автоответчик (Smart Auto-Responder):
- Автоматически проверяет, чем ты сейчас занят в Discord (играешь в CS2, Dota 2, Roblox, слушаешь трек в Spotify или работаешь в Google Antigravity).
- Отвечает чистым естественным текстом без смайликов и шаблонного слопа.
- Кулдаун для защиты от спама (отвечает человеку один раз за 5 минут).
- Самотест: напиши `!test` в любой чат Discord, чтобы проверить работу.

#### ☁️ Облако 24/7 (Render.com / VPS):
- Встроенный веб-сервер для прохождения проверок Render Free Web Service.
- Бот и Telegram-мост работают даже при выключенном компьютере.

---

### 🚀 Быстрый старт

#### 1. Создание Telegram бота (1 минута):
1. Открой [@BotFather](https://t.me/BotFather) в Telegram и отправь `/newbot`.
2. Придумай имя и юзернейм, скопируй полученный **HTTP API Token**.
3. Узнай свой цифровой Chat ID через бота [@userinfobot](https://t.me/userinfobot) (строка `Id`).

#### 2. Настройка `config.json`:
```json
{
    "token": "ТВОЙ_ТОКЕН_DISCORD",
    "cooldown_seconds": 300,
    "only_dms": true,
    "ignored_user_ids": [],
    "telegram": {
        "enabled": true,
        "bot_token": "ТВОЙ_ТОКЕН_TELEGRAM_БОТА",
        "chat_id": 123456789,
        "forward_dms": true,
        "auto_reply_enabled": true
    }
}
```

#### 3. Запуск:
```bash
pip install -r requirements.txt
python autoresponder.py
```

---

### ☁️ Облачный деплой 24/7 на Render.com

В настройках сервиса на Render в разделе **Environment Variables** просто добавь:
- `DISCORD_TOKEN`: токен твоего аккаунта Discord
- `TELEGRAM_BOT_TOKEN`: токен бота от BotFather
- `TELEGRAM_CHAT_ID`: твой личный Telegram ID
- `RENDER`: `true`

---

<a name="english"></a>
## 🇬🇧 English Documentation

### ✨ Features
- **📱 2-Way Telegram Bridge**:
  - Real-time forwarding of incoming Discord DMs to your personal Telegram.
  - **Swipe-to-Reply**: Reply to forwarded messages directly from Telegram to send responses back to Discord.
  - Commands: `/status`, `/toggle` (mute autoresponder), `/send <user_id> <text>`, `/help`.
- **🧠 Contextual Auto-Responder**: Detects active games, Spotify, or Antigravity to craft natural, emoji-free replies.
- **⏱️ Anti-Spam Protection**: Configurable per-user cooldown.
- **☁️ Cloud 24/7 Ready**: Built-in HTTP keep-alive server for Render.com free tier.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
