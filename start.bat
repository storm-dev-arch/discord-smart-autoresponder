@echo off
chcp 65001 >nul
title Discord Auto-Responder
echo Запуск Discord Автоответчика...
"C:\Users\storm\AppData\Local\Programs\Python\Python314\python.exe" "%~dp0autoresponder.py"
pause
