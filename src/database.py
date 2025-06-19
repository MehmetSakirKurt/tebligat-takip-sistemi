#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Uygulama dizininde veritabanı dosyası oluştur
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(app_dir, "tebligat.db")
        else:
            self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat ve tabloları oluştur"""
        print(f"Veritabanı dosyası: {self.db_path}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS petitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                karar_no TEXT NOT NULL,
                dosya_no TEXT,
                tebligat_tarihi DATE NOT NULL,
                yasal_sure INTEGER NOT NULL,
                notlar TEXT,
                sunum_tarihi DATE NOT NULL,
                teslim_tarihi DATE NOT NULL,
                durum TEXT DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_petition(self, karar_no: str, dosya_no: str, tebligat_tarihi: str, 
                    yasal_sure: int, notlar: str = "") -> int:
        """Yeni dilekçe ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tarihleri hesapla
        tebligat_dt = datetime.strptime(tebligat_tarihi, "%Y-%m-%d")
        teslim_dt = tebligat_dt + timedelta(days=yasal_sure)
        sunum_dt = teslim_dt - timedelta(days=2)
        
        cursor.execute('''
            INSERT INTO petitions (karar_no, dosya_no, tebligat_tarihi, yasal_sure, 
                                 notlar, sunum_tarihi, teslim_tarihi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, 
              sunum_dt.strftime("%Y-%m-%d"), teslim_dt.strftime("%Y-%m-%d")))
        
        petition_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return petition_id
    
    def get_all_petitions(self) -> List[Tuple]:
        """Tüm aktif dilekçeleri getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, karar_no, dosya_no, tebligat_tarihi, yasal_sure, 
                   notlar, sunum_tarihi, teslim_tarihi, durum
            FROM petitions 
            WHERE durum = 'aktif'
            ORDER BY teslim_tarihi ASC
        ''')
        
        petitions = cursor.fetchall()
        conn.close()
        
        return petitions
    
    def get_petition_by_id(self, petition_id: int) -> Optional[Tuple]:
        """ID'ye göre dilekçe getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, karar_no, dosya_no, tebligat_tarihi, yasal_sure, 
                   notlar, sunum_tarihi, teslim_tarihi, durum
            FROM petitions 
            WHERE id = ?
        ''', (petition_id,))
        
        petition = cursor.fetchone()
        conn.close()
        
        return petition
    
    def update_petition(self, petition_id: int, karar_no: str, dosya_no: str, 
                       tebligat_tarihi: str, yasal_sure: int, notlar: str = ""):
        """Dilekçe güncelle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tarihleri yeniden hesapla
        tebligat_dt = datetime.strptime(tebligat_tarihi, "%Y-%m-%d")
        teslim_dt = tebligat_dt + timedelta(days=yasal_sure)
        sunum_dt = teslim_dt - timedelta(days=2)
        
        cursor.execute('''
            UPDATE petitions 
            SET karar_no = ?, dosya_no = ?, tebligat_tarihi = ?, yasal_sure = ?, 
                notlar = ?, sunum_tarihi = ?, teslim_tarihi = ?, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar,
              sunum_dt.strftime("%Y-%m-%d"), teslim_dt.strftime("%Y-%m-%d"), 
              petition_id))
        
        conn.commit()
        conn.close()
    
    def archive_petition(self, petition_id: int):
        """Dilekçeyi arşivle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE petitions 
            SET durum = 'arşivlendi', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (petition_id,))
        
        conn.commit()
        conn.close()
    
    def delete_petition(self, petition_id: int):
        """Dilekçeyi sil"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM petitions WHERE id = ?', (petition_id,))
        
        conn.commit()
        conn.close()
    
    def get_upcoming_deadlines(self, days_ahead: int = 7) -> List[Tuple]:
        """Yaklaşan son teslim tarihlerini getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        deadline = today + timedelta(days=days_ahead)
        
        cursor.execute('''
            SELECT id, karar_no, dosya_no, sunum_tarihi, teslim_tarihi
            FROM petitions 
            WHERE durum = 'aktif' AND teslim_tarihi <= ? AND teslim_tarihi >= ?
            ORDER BY teslim_tarihi ASC
        ''', (deadline.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))
        
        petitions = cursor.fetchall()
        conn.close()
        
        return petitions