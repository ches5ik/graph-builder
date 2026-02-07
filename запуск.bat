@echo off
chcp 65001 > nul
title Graph Builder
echo Запуск Graph Builder...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
pause