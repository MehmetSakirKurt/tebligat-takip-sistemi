#!/usr/bin/env python3
"""
Windows için en güvenli çalıştırma scripti
Hiçbir locale problemi yaşanmaz
"""

import sys
import os

def main():
    """Ana fonksiyon"""
    print("Tebligat Takip Sistemi - Windows (Güvenli Sürüm)")
    print("=" * 50)
    
    # Python versiyonunu kontrol et
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ gerekli. Mevcut: {version.major}.{version.minor}")
        input("Devam etmek için Enter'a basın...")
        return 1
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Tkinter kontrolü
    try:
        import tkinter
        print("✅ tkinter bulundu")
    except ImportError:
        print("❌ tkinter bulunamadı! Windows'ta normalde yüklü gelir.")
        print("Python'u yeniden kurun: https://www.python.org/downloads/")
        input("Devam etmek için Enter'a basın...")
        return 1
    
    # Çalıştırma
    try:
        print("\\n🚀 Uygulama başlatılıyor...")
        print("-" * 30)
        
        # Basit sürümü çalıştır
        from src.main_simple import main as app_main
        app_main()
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n👋 Kullanıcı tarafından kapatıldı")
        return 0
    except Exception as e:
        print(f"\\n❌ Hata: {e}")
        print("\\nDetaylı hata:")
        import traceback
        traceback.print_exc()
        input("\\nDevam etmek için Enter'a basın...")
        return 1

if __name__ == "__main__":
    sys.exit(main())