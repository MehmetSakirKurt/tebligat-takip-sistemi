#!/usr/bin/env python3
"""
Tebligat Takip Sistemi Test Runner
Bu script tüm testleri çalıştırır ve sonuçları gösterir.
"""

import unittest
import sys
import os

# Test modüllerini import et
def run_all_tests():
    """Tüm testleri çalıştır"""
    # Test dizinini Python path'ine ekle
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    if test_dir not in sys.path:
        sys.path.insert(0, test_dir)
    
    # Test loader oluştur
    loader = unittest.TestLoader()
    
    # Test suite oluştur
    suite = unittest.TestSuite()
    
    # Test dosyalarını yükle
    try:
        # Database testleri
        from tests.test_database import TestDatabase
        suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
        
        print("✅ Test modülleri başarıyla yüklendi")
        
    except ImportError as e:
        print(f"❌ Test modülleri yüklenirken hata: {e}")
        return False
    
    # Test runner oluştur
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Testleri çalıştır
    print("\n" + "="*50)
    print("TEBLIGAT TAKİP SİSTEMİ TESTLERİ")
    print("="*50)
    
    result = runner.run(suite)
    
    # Sonuçları özetle
    print("\n" + "="*50)
    print("TEST SONUÇLARI")
    print("="*50)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"Toplam Test: {total_tests}")
    print(f"✅ Başarılı: {passed}")
    print(f"❌ Başarısız: {failures}")
    print(f"🚨 Hata: {errors}")
    
    if result.failures:
        print("\nBAŞARISIZ TESTLER:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if result.errors:
        print("\nHATALI TESTLER:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success = failures == 0 and errors == 0
    
    if success:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
    else:
        print("\n⚠️  Bazı testler başarısız oldu!")
    
    return success

def check_dependencies():
    """Gerekli paketlerin yüklü olup olmadığını kontrol et"""
    required_packages = ['ttkbootstrap', 'tkcalendar', 'plyer']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Eksik paketler:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\\nEksik paketleri yüklemek için:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ Tüm gerekli paketler yüklü")
    return True

def main():
    """Ana fonksiyon"""
    print("Tebligat Takip Sistemi - Test Runner")
    print("="*40)
    
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        return 1
    
    # Testleri çalıştır
    success = run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())