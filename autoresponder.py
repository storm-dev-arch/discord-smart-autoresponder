import json
import os
import sys
import time
import io
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
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
        self.wfile.write(b"Antigravity Discord Auto-Responder is Alive!")

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
    if not os.path.exists(CONFIG_PATH):
        default_config = {
            "token": "PASTE_YOUR_DISCORD_TOKEN_HERE",
            "cooldown_seconds": 300,
            "only_dms": True,
            "ignored_user_ids": []
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
TOKEN = os.environ.get("DISCORD_TOKEN") or config.get("token", "").strip()

if not TOKEN or TOKEN == "PASTE_YOUR_DISCORD_TOKEN_HERE":
    print("=" * 60)
    print("[!] ОШИБКА: Токен не указан! Укажи в config.json или переменной DISCORD_TOKEN.")
    print("=" * 60)
    if not os.environ.get("RENDER"):
        input("\nНажми Enter для выхода...")
    sys.exit(1)

client = discord.Client()
last_replied = {}

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
    # 1. Поиск активности через гильдии (сервера)
    activities = []
    for guild in client.guilds:
        if guild.me and guild.me.activities:
            activities = guild.me.activities
            break

    for act in activities:
        # Spotify
        if isinstance(act, discord.Spotify):
            return f"Привет. Я сейчас слушаю трек {act.title} ({act.artist}) и занят делами. Отвечу позже."

        # Пропускаем чистый пользовательский статус, если это не игра
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

    # 2. Если в дискорде активность пустая, проверяем процессы Windows
    hint = get_active_process_hint()
    if hint:
        if "Antigravity" in hint:
            return "Привет. Я сейчас занят, работаю в Google Antigravity. Отвечу позже."
        return f"Привет. Я сейчас занят в {hint}. Освобожусь и напишу."

    # 3. Дефолтный ответ при отсутствии активности
    return "Привет. Меня сейчас нет на месте или я отошел. Отвечу чуть позже."

@client.event
async def on_ready():
    print("=" * 60)
    print(f"[+] Умный автоответчик в сети!")
    print(f"[+] Аккаунт: {client.user} (ID: {client.user.id})")
    print(f"[+] Режим: {'Только ЛС (DMs)' if config.get('only_dms', True) else 'Все чаты'}")
    print(f"[+] Без эмодзи: Да (чистый текст)")
    print(f"[+] Умный статус активности: Включен")
    print("=" * 60)
    print("[i] Для проверки напиши !test в любой чат.")
    print("=" * 60)

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

    # Только ЛС
    if config.get("only_dms", True) and not isinstance(message.channel, discord.DMChannel):
        return

    # Черный список
    if message.author.id in config.get("ignored_user_ids", []):
        return

    user_id = message.author.id
    now = time.time()
    cooldown = config.get("cooldown_seconds", 300)

    # Проверка кулдауна
    if user_id in last_replied:
        elapsed = now - last_replied[user_id]
        if elapsed < cooldown:
            remaining = int(cooldown - elapsed)
            print(f"[-] Пропуск {message.author}: кулдаун еще {remaining} сек.")
            return

    smart_reply = generate_smart_reply()

    try:
        async with message.channel.typing():
            await asyncio.sleep(1.5)
        
        await message.channel.send(smart_reply)
        last_replied[user_id] = now
        print(f"[✓] [{time.strftime('%H:%M:%S')}] Автоответ для {message.author}: \"{smart_reply}\"")
    except Exception as e:
        print(f"[x] Ошибка отправки: {e}")

try:
    client.run(TOKEN, reconnect=True)
except discord.LoginFailure:
    print("\n[!] ОШИБКА: Неверный токен Discord! Проверь config.json.")
    input("\nНажми Enter для выхода...")
except Exception as e:
    print(f"\n[!] Ошибка сессии: {e}")
    input("\nНажми Enter для выхода...")
