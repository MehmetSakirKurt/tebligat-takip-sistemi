@echo off
chcp 65001 >nul 2>&1
echo Tebligat Takip Sistemi - Guvenli Baslatma
echo ==========================================

REM Dosya varlığını kontrol et
if not exist "src\main_simple.py" (
    echo HATA: src\main_simple.py dosyasi bulunamadi!
    echo Lutfen dogru klasorde oldugunuzdan emin olun.
    pause
    exit /b 1
)

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadı! 
    echo Python 3.8+ yükleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python bulundu. Uygulama baslatiliyor...
echo.

REM Güvenli scripti çalıştır
python run_windows_safe.py

if errorlevel 1 (
    echo.
    echo Bir hata olustu!
    pause
)

echo.
echo Uygulama kapandi.
pause