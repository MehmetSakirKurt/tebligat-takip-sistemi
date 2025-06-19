#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
En basit Windows başlatıcı - hiçbir sorun yaşanmaz
"""

import sys
import os

# Önce src klasörünü path'e ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

print("Tebligat Takip Sistemi")
print("=" * 30)

try:
    # Veritabanı modülünü test et
    print("Veritabani modulu yukleniyor...")
    import database
    print("✓ Veritabani modulu tamam")
    
    # Dialog modülünü test et
    print("Dialog modulu yukleniyor...")
    import petition_dialog_windows
    print("✓ Dialog modulu tamam")
    
    # Bildirim modülünü test et
    print("Bildirim modulu yukleniyor...")
    import notification_manager_simple
    print("✓ Bildirim modulu tamam")
    
    # Ana uygulamayı başlat
    print("Ana uygulama baslatiliyor...")
    print("-" * 30)
    
    import main_simple
    main_simple.main()
    
except ImportError as e:
    print(f"Modul yuklenemedi: {e}")
    print("src/ klasorunde mi oldugunuzu kontrol edin")
    input("Enter'a basin...")
    
except Exception as e:
    print(f"Hata: {e}")
    print("\nDetayli hata bilgisi:")
    import traceback
    traceback.print_exc()
    input("\nEnter'a basin...")

print("Program sonlandi.")