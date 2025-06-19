@echo off
echo Tebligat Takip Sistemi - Güvenli Başlatma
echo ==========================================

REM Dosya varlığını kontrol et
if not exist "src\main_simple.py" (
    echo HATA: src\main_simple.py dosyası bulunamadı!
    echo Lütfen doğru klasörde olduğunuzdan emin olun.
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

echo Python bulundu. Uygulama başlatılıyor...
echo.

REM Güvenli scripti çalıştır
python run_windows_safe.py

if errorlevel 1 (
    echo.
    echo Bir hata oluştu!
    pause
)

echo.
echo Uygulama kapandı.
pause