# 🤖 Discord Smart DM Auto-Responder

<p align="center">
  <b>Context-aware Discord DM Auto-Responder with Activity Detection, Anti-Spam Cooldown & 24/7 Cloud Support</b><br>
  <i>Умный автоответчик для Discord в ЛС с определением игр/Spotify, защитой от спама и хостингом 24/7</i>
</p>

<p align="center">
  <a href="#russian">🇷🇺 Читать на русском</a> • <a href="#english">🇬🇧 English Readme</a>
</p>

<p align="center">
  <a href="https://github.com/storm-dev-arch/discord-smart-autoresponder/releases"><img src="https://img.shields.io/github/v/release/storm-dev-arch/discord-smart-autoresponder?color=blue&style=for-the-badge" alt="Release"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Cloud-Render.com%2024%2F7-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render.com">
  <img src="https://img.shields.io/badge/Library-discord.py--self-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py-self">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

<a name="russian"></a>
## 🇷🇺 Документация на русском

### ✨ Возможности
- **🧠 Умные ответы под твою активность**:
  - Автоматически проверяет, чем ты сейчас занят в Discord (играешь в CS2, Dota 2, Roblox, слушаешь Spotify или кодишь в Antigravity).
  - Формирует реалистичный текстовый ответ без кринжовых эмодзи и бот-шаблонов.
- **⏱️ Защита от спама (Smart Cooldown)**:
  - Отвечает человеку только один раз за выбранный период (по умолчанию раз в 5 минут).
  - Все последующие сообщения игнорируются до истечения таймера.
- **🧪 Встроенный самотест (`!test`)**:
  - Напиши `!test` в любой свой чат или ЛС — бот сразу же сформирует и отправит тестовый ответ, чтобы можно было проверить статус без друзей и твинков.
- **☁️ Облачный деплой 24/7 (Render.com / Docker / VPS)**:
  - Встроенный микро веб-сервер на `$PORT` для бесплатного тарифа Render.com.
  - Работает даже при полностью выключенном компьютере.

### 🚀 Быстрый запуск локально
```bash
git clone https://github.com/storm-dev-arch/discord-smart-autoresponder.git
cd discord-smart-autoresponder
pip install -r requirements.txt
cp config.example.json config.json
```
Вставь токен в `config.json` и запусти:
```bash
python autoresponder.py
```

### ☁️ Хостинг 24/7 на Render.com
1. Сделай форк или подключи репозиторий в [dashboard.render.com](https://dashboard.render.com).
2. Создай новый **Web Service** с бесплатным тарифом `Free`.
3. В Environment Variables укажи:
   - `DISCORD_TOKEN`: твой токен Discord
   - `RENDER`: `true`
4. Нажми Deploy — бот поднимется в облаке и будет работать круглосуточно.

---

<a name="english"></a>
## 🇬🇧 English Documentation

### ✨ Features
- **🧠 Activity-Aware Dynamic Replies**: Automatically detects games, Spotify, Antigravity, and active windows to form natural responses without emojis.
- **⏱️ Anti-Spam Smart Cooldown**: Configurable per-user cooldown timer (default: 300s).
- **🧪 Built-in Self-Testing (`!test`)**: Trigger an instant verification test by sending `!test`.
- **☁️ 24/7 Cloud Ready (Render.com / Docker / VPS)**: Built-in HTTP health check server for free tier keep-alive.

### 🚀 Quick Start
```bash
git clone https://github.com/storm-dev-arch/discord-smart-autoresponder.git
cd discord-smart-autoresponder
pip install -r requirements.txt
python autoresponder.py
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
