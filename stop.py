import psutil
import os

count = 0
current_pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['pid'] != current_pid:
            cmd = " ".join(proc.info.get('cmdline') or [])
            if "autoresponder.py" in cmd:
                proc.kill()
                count += 1
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

if count > 0:
    print(f"[+] Автоответчик остановлен (завершено процессов: {count}).")
else:
    print("[-] Автоответчик не был запущен.")
