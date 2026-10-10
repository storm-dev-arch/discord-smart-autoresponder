import json
import os
import sys
import time
import io
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import aiohttp
import psutil
import discord

# Предотвращение падения в pythonw.exe
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# Легковесный веб-сервер для прохождения проверок Render.com
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Antigravity Discord & Telegram Bridge is Alive!")

    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

if os.environ.get("PORT") or os.environ.get("RENDER"):
    t = threading.Thread(target=start_health_server, daemon=True)
    t.start()

# Проверка единственного экземпляра (только для локальной Windows)
if not os.environ.get("RENDER"):
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] != current_pid:
                cmd = " ".join(proc.info.get('cmdline') or [])
                if "autoresponder.py" in cmd:
                    sys.exit(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    default_config = {
        "token": "PASTE_YOUR_DISCORD_TOKEN_HERE",
        "cooldown_seconds": 300,
        "only_dms": True,
        "ignored_user_ids": [],
        "telegram": {
            "enabled": False,
            "bot_token": "",
            "chat_id": 0,
            "forward_dms": True,
            "auto_reply_enabled": True
        }
    }
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if "telegram" not in cfg:
                cfg["telegram"] = default_config["telegram"]
            return cfg
    except Exception:
        return default_config

config = load_config()

# Загрузка токенов из переменных окружения или конфига
TOKEN = os.environ.get("DISCORD_TOKEN") or config.get("token", "").strip()

TG_ENABLED = os.environ.get("TELEGRAM_ENABLED", "").lower() in ["1", "true"] or config.get("telegram", {}).get("enabled", False)
TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or config.get("telegram", {}).get("bot_token", "").strip()
raw_chat_id = os.environ.get("TELEGRAM_CHAT_ID") or config.get("telegram", {}).get("chat_id", 0)
try:
    TG_CHAT_ID = int(raw_chat_id)
except (ValueError, TypeError):
    TG_CHAT_ID = 0

if TG_BOT_TOKEN and TG_CHAT_ID != 0:
    TG_ENABLED = True

if not TOKEN or TOKEN == "PASTE_YOUR_DISCORD_TOKEN_HERE":
    print("=" * 60)
    print("[!] ОШИБКА: Токен Discord не указан!")
    print("=" * 60)
    if not os.environ.get("RENDER"):
        input("\nНажми Enter для выхода...")
    sys.exit(1)

client = discord.Client()
last_replied = {}
active_replying_users = set()
# Маппинг для связи сообщений: telegram_message_id -> {channel_id, discord_msg_id, author, user_id}
tg_to_discord_map = {}
# Флаг включения автоответчика (можно переключать через Telegram командой /toggle)
auto_reply_active = config.get("telegram", {}).get("auto_reply_enabled", True)

def get_active_process_hint():
    """Проверка фоновых процессов, если активность Дискорда еще не обновилась."""
    proc_map = {
        "antigravity.exe": "Google Antigravity",
        "Code.exe": "VS Code",
        "cs2.exe": "Counter-Strike 2",
        "dota2.exe": "Dota 2",
        "RobloxPlayerBeta.exe": "Roblox",
        "javaw.exe": "Minecraft",
        "Telegram.exe": "Telegram",
        "Photoshop.exe": "Photoshop",
        "Blender.exe": "Blender",
        "Unity.exe": "Unity",
        "UnrealEditor.exe": "Unreal Engine"
    }
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info.get('name')
            if name in proc_map:
                return proc_map[name]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def generate_smart_reply():
    """Формирует контекстный умный ответ на основе текущей активности Discord (без эмодзи)."""
    activities = []
    for guild in client.guilds:
        if guild.me and guild.me.activities:
            activities = guild.me.activities
            break

    for act in activities:
        if isinstance(act, discord.Spotify):
            return f"Привет. Я сейчас слушаю трек {act.title} ({act.artist}) и занят делами. Отвечу позже."

        if act.type == discord.ActivityType.custom:
            continue

        act_name = getattr(act, "name", "")
        details = getattr(act, "details", None)
        state = getattr(act, "state", None)

        if act_name:
            if "antigravity" in act_name.lower():
                if details:
                    return f"Привет. Я сейчас занят, работаю в Google Antigravity ({details}). Напишу позже."
                return "Привет. Я сейчас занят, работаю в Google Antigravity. Напишу позже."
            
            if act.type == discord.ActivityType.playing:
                extra = f" ({state})" if state else ""
                return f"Привет. Я сейчас в игре {act_name}{extra}. Как освобожусь, сразу отвечу."
            
            if act.type == discord.ActivityType.streaming:
                return f"Привет. Я сейчас стримлю {act_name}. Отвечу после завершения стрима."
            
            if act.type == discord.ActivityType.watching:
                return f"Привет. Я сейчас смотрю {act_name}. Отвечу позже."
            
            if act.type == discord.ActivityType.listening:
                return f"Привет. Я сейчас слушаю {act_name}. Отвечу чуть позже."

            return f"Привет. Я сейчас занят в {act_name}. Отвечу позже."

    hint = get_active_process_hint()
    if hint:
        if "Antigravity" in hint:
            return "Привет. Я сейчас занят, работаю в Google Antigravity. Отвечу позже."
        return f"Привет. Я сейчас занят в {hint}. Освобожусь и напишу."

    return "Привет. Меня сейчас нет на месте или я отошел. Отвечу чуть позже."

# ----------------- TELEGRAM BRIDGE API -----------------

async def tg_send_message(text, parse_mode="HTML", reply_to_message_id=None):
    """Отправка сообщения в Telegram владельцу."""
    if not TG_ENABLED or not TG_BOT_TOKEN or not TG_CHAT_ID:
        return None
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("result", {}).get("message_id")
                else:
                    err = await resp.text()
                    print(f"[x] Ошибка отправки в Telegram: {resp.status} - {err}")
    except Exception as e:
        print(f"[x] Исключение при отправке в Telegram: {e}")
    return None

async def telegram_worker():
    """Фоновый поллер входящих сообщений и команд из Telegram."""
    if not TG_ENABLED or not TG_BOT_TOKEN or not TG_CHAT_ID:
        return

    offset = 0
    print("[+] Telegram Bridge запущен и слушает входящие команды/ответы...")
    global auto_reply_active

    await tg_send_message(
        f"🤖 <b>Discord Bridge подключен!</b>\n"
        f"👤 Аккаунт: <code>{client.user}</code>\n"
        f"⚡ Автоответчик: {'ВКЛ' if auto_reply_active else 'ВЫКЛ'}\n\n"
        f"<i>Теперь все входящие ЛС будут прилетать сюда. Просто отвечай свайпом на сообщение, чтобы написать человеку в Discord!</i>"
    )

    while not client.is_closed():
        try:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates"
            params = {"offset": offset, "timeout": 25}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for update in data.get("result", []):
                            offset = update["update_id"] + 1
                            msg = update.get("message")
                            if not msg:
                                continue

                            sender_id = msg.get("from", {}).get("id")
                            if sender_id != TG_CHAT_ID:
                                continue  # Игнорировать посторонних

                            text = msg.get("text", "").strip()
                            reply_to = msg.get("reply_to_message")
                            msg_id = msg.get("message_id")

                            # 1. Ответ свайпом на пересланное сообщение из Discord
                            if reply_to and reply_to.get("message_id") in tg_to_discord_map:
                                mapping = tg_to_discord_map[reply_to["message_id"]]
                                ch_id = mapping["channel_id"]
                                discord_msg_id = mapping.get("discord_msg_id")
                                author_name = mapping.get("author", "пользователю")
                                target_uid = mapping.get("user_id")

                                try:
                                    ch = client.get_channel(ch_id) or await client.fetch_channel(ch_id)
                                    async with ch.typing():
                                        await asyncio.sleep(0.8)

                                    # Отвечаем именно как Reply на исходное сообщение в Discord
                                    sent_msg = None
                                    if discord_msg_id:
                                        try:
                                            ref_msg = await ch.fetch_message(discord_msg_id)
                                            sent_msg = await ref_msg.reply(text, mention_author=True)
                                        except Exception:
                                            pass
                                    if not sent_msg:
                                        sent_msg = await ch.send(text)

                                    # Продлеваем таймаут автоответчика на 10 минут, раз мы сами ответили человеку
                                    if target_uid:
                                        last_replied[target_uid] = time.time() + 600

                                    await tg_send_message(
                                        f"✅ Отправлено ответом в Discord для <b>{author_name}</b>",
                                        reply_to_message_id=msg_id
                                    )
                                    print(f"[✓] Ответ из TG отправлен в Discord ({author_name}): {text[:30]}")
                                except Exception as send_err:
                                    await tg_send_message(
                                        f"❌ Ошибка отправки в Discord: <code>{send_err}</code>",
                                        reply_to_message_id=msg_id
                                    )
                                continue

                            # 2. Обработка команд
                            if text.startswith("/"):
                                cmd_parts = text.split(maxsplit=1)
                                cmd = cmd_parts[0].lower().split("@")[0]
                                args = cmd_parts[1] if len(cmd_parts) > 1 else ""

                                if cmd in ["/start", "/help"]:
                                    help_text = (
                                        "📖 <b>Команды Telegram Bridge:</b>\n\n"
                                        "• <b>Ответ свайпом</b> — просто свайпни любое сообщение от бота и напиши ответ. Он сразу улетит человеку в Discord.\n"
                                        "• <code>/status</code> — статус подключения и активности Discord.\n"
                                        "• <code>/toggle</code> — включить/выключить автоответчик.\n"
                                        "• <code>/send &lt;user_id&gt; &lt;текст&gt;</code> — отправить ЛС по ID.\n"
                                        "• <code>/help</code> — это меню."
                                    )
                                    await tg_send_message(help_text, reply_to_message_id=msg_id)

                                elif cmd == "/status":
                                    cur_act = generate_smart_reply()
                                    status_msg = (
                                        f"📊 <b>Статус моста:</b>\n"
                                        f"• Discord: <code>{client.user}</code> (ID: <code>{client.user.id}</code>)\n"
                                        f"• Автоответчик: {'🟢 ВКЛ' if auto_reply_active else '🔴 ВЫКЛ'}\n"
                                        f"• Текущая активность: <i>{cur_act}</i>\n"
                                        f"• Пинг Discord: <code>{round(client.latency * 1000)}ms</code>"
                                    )
                                    await tg_send_message(status_msg, reply_to_message_id=msg_id)

                                elif cmd == "/toggle":
                                    auto_reply_active = not auto_reply_active
                                    state_str = "ВКЛЮЧЕН 🟢" if auto_reply_active else "ВЫКЛЮЧЕН (режим ручного общения) 🔴"
                                    await tg_send_message(
                                        f"⚡ Автоответчик теперь <b>{state_str}</b>",
                                        reply_to_message_id=msg_id
                                    )

                                elif cmd == "/send":
                                    # /send <user_id> <сообщение>
                                    sub_parts = args.split(maxsplit=1)
                                    if len(sub_parts) < 2:
                                        await tg_send_message("ℹ️ Использование: <code>/send &lt;ID_пользователя&gt; &lt;текст&gt;</code>", reply_to_message_id=msg_id)
                                    else:
                                        target_uid, out_text = sub_parts[0], sub_parts[1]
                                        try:
                                            target_user = await client.fetch_user(int(target_uid))
                                            dm_channel = await target_user.create_dm()
                                            await dm_channel.send(out_text)
                                            await tg_send_message(f"✅ Отправлено в ЛС для <b>{target_user}</b>", reply_to_message_id=msg_id)
                                        except Exception as e:
                                            await tg_send_message(f"❌ Ошибка отправки: <code>{e}</code>", reply_to_message_id=msg_id)

                                elif cmd == "/help":
                                    help_text = (
                                        "📖 <b>Команды Telegram Bridge:</b>\n\n"
                                        "• <b>Ответ свайпом</b> — просто свайпни любое сообщение от бота и напиши ответ. Он сразу улетит человеку в Discord.\n"
                                        "• <code>/status</code> — статус подключения и активности Discord.\n"
                                        "• <code>/toggle</code> — включить/выключить автоответчик.\n"
                                        "• <code>/send &lt;user_id&gt; &lt;текст&gt;</code> — отправить ЛС по ID.\n"
                                        "• <code>/help</code> — это меню."
                                    )
                                    await tg_send_message(help_text, reply_to_message_id=msg_id)
        except Exception as poll_err:
            await asyncio.sleep(4)
        await asyncio.sleep(0.5)

# ----------------- DISCORD EVENTS -----------------

@client.event
async def on_ready():
    print("=" * 60)
    print(f"[+] Discord клиент подключен!")
    print(f"[+] Аккаунт: {client.user} (ID: {client.user.id})")
    print(f"[+] Telegram Bridge: {'ВКЛЮЧЕН' if TG_ENABLED else 'ВЫКЛЮЧЕН'}")
    print(f"[+] Автоответчик: {'ВКЛЮЧЕН' if auto_reply_active else 'ВЫКЛЮЧЕН'}")
    print("=" * 60)
    if TG_ENABLED:
        asyncio.create_task(telegram_worker())

@client.event
async def on_message(message):
    # Тест от самого себя через !test
    if message.author.id == client.user.id:
        if message.content.strip().lower() == "!test":
            reply_text = generate_smart_reply()
            try:
                async with message.channel.typing():
                    await asyncio.sleep(1.0)
                await message.channel.send(f"[Тест автоответчика]: {reply_text}")
                print(f"[✓] [{time.strftime('%H:%M:%S')}] Тест сработал: \"{reply_text}\"")
            except Exception as e:
                print(f"[x] Ошибка теста: {e}")
        return

    # Игнорировать ботов
    if message.author.bot:
        return

    # Строгая проверка: ТОЛЬКО личные сообщения 1 на 1 (игнорировать сервера и групповые чаты)
    if message.guild is not None:
        return
    if not isinstance(message.channel, discord.DMChannel):
        return
    if isinstance(message.channel, discord.GroupChannel):
        return

    # Черный список
    if message.author.id in config.get("ignored_user_ids", []):
        return

    user_id = message.author.id
    now = time.time()
    cooldown = config.get("cooldown_seconds", 300)

    # 1. ПЕРЕСЫЛКА В ТЕЛЕГРАМ
    if TG_ENABLED:
        sender_tag = f"{message.author.name}#{message.author.discriminator}" if message.author.discriminator != "0" else message.author.name
        attachments_text = ""
        if message.attachments:
            att_urls = "\n".join([f"📎 <a href='{att.url}'>Вложение</a>" for att in message.attachments])
            attachments_text = f"\n{att_urls}"

        clean_content = message.clean_content.replace("<", "&lt;").replace(">", "&gt;") if message.clean_content else "<i>[Вложение / Пустое]</i>"

        tg_text = (
            f"📨 <b>Новое сообщение в Discord (ЛС)!</b>\n"
            f"👤 <b>От:</b> {sender_tag} (<code>{message.author.id}</code>)\n\n"
            f"💬 {clean_content}"
            f"{attachments_text}\n\n"
            f"<i>💡 Ответь свайпом на это сообщение, чтобы ответить в Discord.</i>"
        )
        tg_msg_id = await tg_send_message(tg_text)
        if tg_msg_id:
            tg_to_discord_map[tg_msg_id] = {
                "channel_id": message.channel.id,
                "discord_msg_id": message.id,
                "author": sender_tag,
                "user_id": user_id
            }

    # 2. АВТООТВЕТЧИК (с жесткой защитой от спама и гонок сообщений)
    if auto_reply_active:
        # Если бот уже прямо сейчас печатает ответ этому пользователю — отбой
        if user_id in active_replying_users:
            return

        # Проверка кулдауна
        if user_id in last_replied:
            elapsed = now - last_replied[user_id]
            if elapsed < cooldown:
                remaining = int(cooldown - elapsed)
                print(f"[-] Пропуск автоответа для {message.author}: кулдаун еще {remaining} сек.")
                return

        # Взводим блокировку и таймер СРАЗУ, до задержки печати!
        active_replying_users.add(user_id)
        last_replied[user_id] = now

        smart_reply = generate_smart_reply()
        try:
            async with message.channel.typing():
                await asyncio.sleep(2.0)
            await message.channel.send(smart_reply)
            print(f"[✓] [{time.strftime('%H:%M:%S')}] Автоответ для {message.author}: \"{smart_reply}\"")
        except Exception as e:
            print(f"[x] Ошибка отправки автоответа: {e}")
        finally:
            active_replying_users.discard(user_id)

try:
    client.run(TOKEN, reconnect=True)
except discord.LoginFailure:
    print("\n[!] ОШИБКА: Неверный токен Discord! Проверь config.json или DISCORD_TOKEN.")
    if not os.environ.get("RENDER"):
        input("\nНажми Enter для выхода...")
except Exception as e:
    print(f"\n[!] Ошибка сессии: {e}")
    if not os.environ.get("RENDER"):
        input("\nНажми Enter для выхода...")
