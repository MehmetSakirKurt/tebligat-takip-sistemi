#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit bildirim yöneticisi - plyer bağımlılığı olmadan
"""
from datetime import datetime, timedelta
import json
import os

class NotificationManager:
    def __init__(self, database):
        self.db = database
        self.notification_history_file = "notification_history.json"
        self.notification_history = self.load_notification_history()
    
    def load_notification_history(self):
        """Bildirim geçmişini yükle"""
        if os.path.exists(self.notification_history_file):
            try:
                with open(self.notification_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_notification_history(self):
        """Bildirim geçmişini kaydet"""
        try:
            with open(self.notification_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.notification_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Bildirim geçmişi kaydedilemedi: {e}")
    
    def should_notify(self, petition_id, notification_type, target_date):
        """Bildirim gönderilmeli mi kontrol et"""
        key = f"{petition_id}_{notification_type}_{target_date}"
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        # Bu bildirim daha önce bugün gönderilmiş mi
        if key in self.notification_history:
            last_sent = self.notification_history[key]
            if last_sent == today:
                return False
        
        return True
    
    def mark_notification_sent(self, petition_id, notification_type, target_date):
        """Bildirimi gönderildi olarak işaretle"""
        key = f"{petition_id}_{notification_type}_{target_date}"
        today = datetime.now().date().strftime("%Y-%m-%d")
        self.notification_history[key] = today
        self.save_notification_history()
    
    def send_notification(self, title, message, timeout=10):
        """Konsola bildirim yazdır (plyer yerine)"""
        try:
            print(f"\n{'='*50}")
            print(f"BILDIRIM: {title}")
            print(f"{'='*50}")
            print(message)
            print(f"{'='*50}\n")
            return True
        except Exception as e:
            print(f"Bildirim gönderilemedi: {e}")
            return False
    
    def check_and_send_notifications(self):
        """Bildirimleri kontrol et ve gerekirse gönder"""
        today = datetime.now().date()
        
        # Aktif dilekçeleri getir
        petitions = self.db.get_all_petitions()
        
        for petition in petitions:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition
            
            # Tarihleri parse et
            sunum_dt = datetime.strptime(sunum_tarihi, "%Y-%m-%d").date()
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            
            # Avukata sunum bildirimi (sunum tarihinde)
            if sunum_dt == today:
                if self.should_notify(id_val, "sunum", sunum_tarihi):
                    title = "🔔 Avukata Sunum Zamanı!"
                    message = f"Karar No: {karar_no}\nBugün avukata sunulmalı!\nSon Teslim: {self.format_date(teslim_tarihi)}"
                    
                    if self.send_notification(title, message):
                        self.mark_notification_sent(id_val, "sunum", sunum_tarihi)
    
    def format_date(self, date_str):
        """Tarihi güzel formatta göster"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d.%m.%Y")
        except:
            return date_str
    
    def test_notification(self):
        """Test bildirimi gönder"""
        title = "Test Bildirimi"
        message = "Tebligat Takip Sistemi bildirim sistemi çalışıyor!"
        return self.send_notification(title, message)
    
    def get_notification_summary(self):
        """Bildirim özetini al"""
        today = datetime.now().date()
        petitions = self.db.get_all_petitions()
        
        summary = {
            'bugun_sunum': 0,
            'yarin_teslim': 0,
            'bugun_teslim': 0,
            'geciken': 0
        }
        
        for petition in petitions:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition
            
            sunum_dt = datetime.strptime(sunum_tarihi, "%Y-%m-%d").date()
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            
            if sunum_dt == today:
                summary['bugun_sunum'] += 1
            elif teslim_dt - today == timedelta(days=1):
                summary['yarin_teslim'] += 1
            elif teslim_dt == today:
                summary['bugun_teslim'] += 1
            elif teslim_dt < today:
                summary['geciken'] += 1
        
        return summary