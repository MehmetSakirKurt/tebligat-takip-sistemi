import unittest
import tempfile
import os
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import Database

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Her test öncesi çalışır"""
        # Geçici veritabanı dosyası oluştur
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
    
    def tearDown(self):
        """Her test sonrası çalışır"""
        # Geçici dosyayı sil
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_petition(self):
        """Dilekçe ekleme testini yap"""
        petition_id = self.db.add_petition(
            karar_no="2024/123",
            dosya_no="2024/456",
            tebligat_tarihi="2024-01-15",
            yasal_sure=30,
            notlar="Test dilekçesi"
        )
        
        self.assertIsInstance(petition_id, int)
        self.assertGreater(petition_id, 0)
        
        # Eklenen dilekçeyi kontrol et
        petition = self.db.get_petition_by_id(petition_id)
        self.assertIsNotNone(petition)
        self.assertEqual(petition[1], "2024/123")  # karar_no
        self.assertEqual(petition[2], "2024/456")  # dosya_no
    
    def test_get_all_petitions(self):
        """Tüm dilekçeleri getirme testini yap"""
        # Birkaç dilekçe ekle
        self.db.add_petition("2024/123", "2024/456", "2024-01-15", 30, "Test 1")
        self.db.add_petition("2024/124", "2024/457", "2024-01-16", 15, "Test 2")
        
        petitions = self.db.get_all_petitions()
        self.assertEqual(len(petitions), 2)
        
        # İlk dilekçe kontrol
        self.assertEqual(petitions[0][1], "2024/123")
        self.assertEqual(petitions[1][1], "2024/124")
    
    def test_date_calculations(self):
        """Tarih hesaplama testini yap"""
        petition_id = self.db.add_petition(
            karar_no="2024/123",
            dosya_no="2024/456",
            tebligat_tarihi="2024-01-15",
            yasal_sure=30
        )
        
        petition = self.db.get_petition_by_id(petition_id)
        
        # Beklenen tarihler
        tebligat_dt = datetime.strptime("2024-01-15", "%Y-%m-%d")
        expected_teslim = tebligat_dt + timedelta(days=30)
        expected_sunum = expected_teslim - timedelta(days=2)
        
        self.assertEqual(petition[6], expected_sunum.strftime("%Y-%m-%d"))  # sunum_tarihi
        self.assertEqual(petition[7], expected_teslim.strftime("%Y-%m-%d"))  # teslim_tarihi
    
    def test_update_petition(self):
        """Dilekçe güncelleme testini yap"""
        petition_id = self.db.add_petition("2024/123", "2024/456", "2024-01-15", 30)
        
        # Güncellemeleri yap
        self.db.update_petition(
            petition_id,
            karar_no="2024/999",
            dosya_no="2024/888",
            tebligat_tarihi="2024-01-20",
            yasal_sure=45,
            notlar="Güncellendi"
        )
        
        # Güncellenmiş dilekçeyi kontrol et
        petition = self.db.get_petition_by_id(petition_id)
        self.assertEqual(petition[1], "2024/999")
        self.assertEqual(petition[2], "2024/888")
        self.assertEqual(petition[4], 45)  # yasal_sure
        self.assertEqual(petition[5], "Güncellendi")  # notlar
    
    def test_archive_petition(self):
        """Dilekçe arşivleme testini yap"""
        petition_id = self.db.add_petition("2024/123", "2024/456", "2024-01-15", 30)
        
        # Arşivle
        self.db.archive_petition(petition_id)
        
        # Aktif dilekçeler listesinde olmamalı
        active_petitions = self.db.get_all_petitions()
        self.assertEqual(len(active_petitions), 0)
        
        # Ama veritabanında hala bulunmalı
        petition = self.db.get_petition_by_id(petition_id)
        self.assertIsNotNone(petition)
        self.assertEqual(petition[8], "arşivlendi")  # durum
    
    def test_delete_petition(self):
        """Dilekçe silme testini yap"""
        petition_id = self.db.add_petition("2024/123", "2024/456", "2024-01-15", 30)
        
        # Sil
        self.db.delete_petition(petition_id)
        
        # Artık bulunmamalı
        petition = self.db.get_petition_by_id(petition_id)
        self.assertIsNone(petition)
    
    def test_get_upcoming_deadlines(self):
        """Yaklaşan son teslim tarihleri testini yap"""
        today = datetime.now().date()
        
        # Bugünden 5 gün sonra teslim
        future_date = today + timedelta(days=5)
        tebligat_date = future_date - timedelta(days=30)  # 30 günlük yasal süre
        
        petition_id = self.db.add_petition(
            "2024/123", 
            "2024/456", 
            tebligat_date.strftime("%Y-%m-%d"), 
            30
        )
        
        # Yaklaşan son teslim tarihlerini getir (7 gün içinde)
        upcoming = self.db.get_upcoming_deadlines(7)
        
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0][1], "2024/123")  # karar_no

if __name__ == '__main__':
    unittest.main()