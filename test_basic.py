#!/usr/bin/env python3
"""
Temel test - bağımlılık olmadan çalışacak basit test
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_database_basic():
    """Veritabanı temel fonksiyonlarını test et"""
    print("🔍 Veritabanı modülü test ediliyor...")
    
    try:
        from database import Database
        
        # Geçici test veritabanı
        import tempfile
        test_db_file = tempfile.mktemp(suffix='.db')
        test_db = Database(test_db_file)
        
        # Dilekçe ekleme testi
        petition_id = test_db.add_petition(
            karar_no="TEST/123",
            dosya_no="TEST/456", 
            tebligat_tarihi="2024-01-15",
            yasal_sure=30,
            notlar="Test dilekçesi"
        )
        
        assert petition_id > 0, "Dilekçe ID pozitif olmalı"
        print("  ✅ Dilekçe ekleme başarılı")
        
        # Dilekçe getirme testi
        petition = test_db.get_petition_by_id(petition_id)
        assert petition is not None, "Dilekçe bulunmalı"
        assert petition[1] == "TEST/123", "Karar numarası eşleşmeli"
        print("  ✅ Dilekçe getirme başarılı")
        
        # Tüm dilekçeler testi
        all_petitions = test_db.get_all_petitions()
        assert len(all_petitions) == 1, "Bir dilekçe olmalı"
        print("  ✅ Tüm dilekçeler getirme başarılı")
        
        # Güncelleme testi
        test_db.update_petition(
            petition_id,
            karar_no="TEST/999",
            dosya_no="TEST/888",
            tebligat_tarihi="2024-01-20",
            yasal_sure=45,
            notlar="Güncellenmiş test"
        )
        
        updated_petition = test_db.get_petition_by_id(petition_id)
        assert updated_petition[1] == "TEST/999", "Karar numarası güncellenmiş olmalı"
        print("  ✅ Dilekçe güncelleme başarılı")
        
        # Arşivleme testi
        test_db.archive_petition(petition_id)
        active_petitions = test_db.get_all_petitions()
        assert len(active_petitions) == 0, "Aktif dilekçe kalmamalı"
        print("  ✅ Dilekçe arşivleme başarılı")
        
        print("✅ Veritabanı modülü tüm testleri geçti!")
        return True
        
    except Exception as e:
        print(f"❌ Veritabanı testi başarısız: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_notification_basic():
    """Bildirim yöneticisini temel seviyede test et"""
    print("🔍 Bildirim modülü test ediliyor...")
    
    try:
        from database import Database
        from notification_manager_simple import NotificationManager
        
        # Test veritabanı
        import tempfile
        test_db_file = tempfile.mktemp(suffix='.db')
        test_db = Database(test_db_file)
        notification_manager = NotificationManager(test_db)
        
        # Temel fonksiyonlar
        assert hasattr(notification_manager, 'check_and_send_notifications'), "check_and_send_notifications metodu olmalı"
        assert hasattr(notification_manager, 'get_notification_summary'), "get_notification_summary metodu olmalı"
        
        # Özet testi
        summary = notification_manager.get_notification_summary()
        assert isinstance(summary, dict), "Özet dictionary olmalı"
        assert 'bugun_sunum' in summary, "bugun_sunum anahtarı olmalı"
        
        print("✅ Bildirim modülü temel testleri geçti!")
        return True
        
    except Exception as e:
        print(f"❌ Bildirim testi başarısız: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Temel import testleri"""
    print("🔍 Modül import'ları test ediliyor...")
    
    try:
        import sqlite3
        print("  ✅ sqlite3 import başarılı")
        
        from datetime import datetime, timedelta
        print("  ✅ datetime import başarılı")
        
        import json
        print("  ✅ json import başarılı")
        
        import os
        print("  ✅ os import başarılı")
        
        print("✅ Tüm temel modüller import edildi!")
        return True
        
    except Exception as e:
        print(f"❌ Import testi başarısız: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("Tebligat Takip Sistemi - Temel Test")
    print("=" * 40)
    
    tests = [
        ("Import Testleri", test_imports),
        ("Veritabanı Testleri", test_database_basic),
        ("Bildirim Testleri", test_notification_basic)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} BAŞARILI\n")
            else:
                print(f"❌ {test_name} BAŞARISIZ\n")
        except Exception as e:
            print(f"❌ {test_name} HATA: {e}\n")
    
    print("=" * 40)
    print("TEST SONUÇLARI")
    print("=" * 40)
    print(f"Toplam: {total}")
    print(f"Başarılı: {passed}")
    print(f"Başarısız: {total - passed}")
    
    if passed == total:
        print("\n🎉 TÜM TEMEL TESTLER BAŞARILI!")
        print("Sistem hazır! Şimdi GUI bileşenlerini kurun:")
        print("pip3 install --user -r requirements.txt")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test başarısız!")
        return 1

if __name__ == "__main__":
    sys.exit(main())