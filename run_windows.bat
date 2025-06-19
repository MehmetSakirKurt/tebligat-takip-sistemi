@echo off
echo Tebligat Takip Sistemi - Windows Launcher
echo =========================================

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadi! Python 3.8+ yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ana scripti çalıştır
python run_windows.py

pause