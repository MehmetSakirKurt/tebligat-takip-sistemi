#!/usr/bin/env python3
"""
Windows için çalıştırma scripti
"""

import sys
import os
import subprocess

def check_python():
    """Python versiyonunu kontrol et"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ gerekli. Mevcut versiyon: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Gerekli paketleri kontrol et"""
    print("Paket kontrolü yapılıyor...")
    
    required_packages = ['tkinter']
    optional_packages = ['ttkbootstrap', 'tkcalendar', 'plyer']
    
    # Zorunlu paketler
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} bulunamadı")
            return False
    
    # İsteğe bağlı paketler
    missing_optional = []
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"⚠️  {package} bulunamadı (isteğe bağlı)")
            missing_optional.append(package)
    
    if missing_optional:
        print(f"\\n📝 İsteğe bağlı paketleri yüklemek için:")
        print(f"pip install {' '.join(missing_optional)}")
        print("\\n⚠️  Bu paketler olmadan da uygulama çalışacak ama daha basit arayüze sahip olacak.")
    
    return True

def run_app():
    """Uygulamayı çalıştır"""
    try:
        # Locale sorununu çöz
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'C')
            print("✅ Locale ayarlandı")
        except:
            print("⚠️  Locale ayarlanamadı, devam ediliyor...")
        
        # Windows'a uygun main dosyasını çalıştır
        if os.path.exists('src/main_simple.py'):
            print("Basit Windows sürümü çalıştırılıyor...")
            import src.main_simple as app
        elif os.path.exists('src/main_windows.py'):
            print("Windows sürümü çalıştırılıyor...")
            import src.main_windows as app
        elif os.path.exists('src/main.py'):
            print("Standart sürüm çalıştırılıyor...")
            import src.main as app
        else:
            print("❌ Ana uygulama dosyası bulunamadı!")
            return False
        
        app.main()
        return True
        
    except KeyboardInterrupt:
        print("\\n👋 Uygulama kullanıcı tarafından kapatıldı")
        return True
    except Exception as e:
        print(f"❌ Uygulama çalıştırılırken hata: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ana fonksiyon"""
    print("Tebligat Takip Sistemi - Windows")
    print("=" * 40)
    
    # Python kontrolü
    if not check_python():
        input("Devam etmek için Enter tuşuna basın...")
        return 1
    
    # Bağımlılık kontrolü
    if not check_dependencies():
        print("\\nGerekli paketleri yüklemek için:")
        print("pip install tkinter")
        input("Devam etmek için Enter tuşuna basın...")
        return 1
    
    print("\\n🚀 Uygulama başlatılıyor...")
    print("-" * 40)
    
    # Uygulamayı çalıştır
    success = run_app()
    
    if not success:
        input("\\nHata oluştu. Devam etmek için Enter tuşuna basın...")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Kritik hata: {e}")
        input("Devam etmek için Enter tuşuna basın...")
        sys.exit(1)