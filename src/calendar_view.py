#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takvim görünümü modülü
"""
import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, timedelta

class CalendarView:
    def __init__(self, parent, database):
        self.parent = parent
        self.db = database
        self.current_date = datetime.now()
        
        self.setup_ui()
        self.load_calendar_data()
        
    def setup_ui(self):
        """Takvim UI'ını oluştur"""
        # Ana frame
        self.main_frame = ttk.Frame(self.parent)
        
        # Üst panel - ay/yıl navigasyon
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Önceki ay butonu
        self.prev_button = ttk.Button(
            nav_frame, 
            text="◀", 
            width=3,
            command=self.prev_month
        )
        self.prev_button.pack(side=tk.LEFT)
        
        # Ay/Yıl etiketi
        self.month_label = ttk.Label(
            nav_frame,
            font=("Arial", 14, "bold")
        )
        self.month_label.pack(side=tk.LEFT, expand=True)
        
        # Sonraki ay butonu
        self.next_button = ttk.Button(
            nav_frame, 
            text="▶", 
            width=3,
            command=self.next_month
        )
        self.next_button.pack(side=tk.RIGHT)
        
        # Bugün butonu
        today_button = ttk.Button(
            nav_frame,
            text="Bugün",
            command=self.go_to_today
        )
        today_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Takvim grid
        self.calendar_frame = ttk.Frame(self.main_frame)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Gün başlıkları
        days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        for i, day in enumerate(days):
            label = ttk.Label(
                self.calendar_frame,
                text=day,
                font=("Arial", 10, "bold"),
                anchor=tk.CENTER,
                relief=tk.RIDGE
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Grid configure
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(7):  # 6 hafta + başlık
            self.calendar_frame.rowconfigure(i, weight=1)
        
        # Alt panel - seçili gün bilgileri
        info_frame = ttk.LabelFrame(self.main_frame, text="Seçili Gün Bilgileri")
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_text = tk.Text(
            info_frame,
            height=4,
            wrap=tk.WORD,
            font=("Arial", 9)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.day_buttons = []
        
    def pack(self, **kwargs):
        """Frame'i pack et"""
        self.main_frame.pack(**kwargs)
    
    def prev_month(self):
        """Önceki aya git"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.load_calendar_data()
    
    def next_month(self):
        """Sonraki aya git"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.load_calendar_data()
    
    def go_to_today(self):
        """Bugüne git"""
        self.current_date = datetime.now()
        self.load_calendar_data()
    
    def load_calendar_data(self):
        """Takvim verilerini yükle"""
        # Ay/Yıl etiketini güncelle
        ay_adlari = [
            '', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
            'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ]
        self.month_label.config(
            text=f"{ay_adlari[self.current_date.month]} {self.current_date.year}"
        )
        
        # Eski butonları temizle
        for button in self.day_buttons:
            button.destroy()
        self.day_buttons.clear()
        
        # Takvim verilerini al
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Dilekçe verilerini al
        petitions = self.db.get_all_petitions()
        petition_dates = {}
        
        for petition in petitions:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition
            
            # Tebligat tarihi
            tebligat_dt = datetime.strptime(tebligat_tarihi, "%Y-%m-%d").date()
            if tebligat_dt not in petition_dates:
                petition_dates[tebligat_dt] = []
            petition_dates[tebligat_dt].append(('Tebligat', karar_no, 'blue'))
            
            # Sunum tarihi
            sunum_dt = datetime.strptime(sunum_tarihi, "%Y-%m-%d").date()
            if sunum_dt not in petition_dates:
                petition_dates[sunum_dt] = []
            petition_dates[sunum_dt].append(('Sunum', karar_no, 'orange'))
            
            # Teslim tarihi
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            if teslim_dt not in petition_dates:
                petition_dates[teslim_dt] = []
            petition_dates[teslim_dt].append(('Teslim', karar_no, 'red'))
        
        # Gün butonlarını oluştur
        today = datetime.now().date()
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Boş gün
                    button = ttk.Label(self.calendar_frame, text="")
                else:
                    # Normal gün
                    try:
                        current_day = datetime(self.current_date.year, self.current_date.month, day).date()
                    except ValueError:
                        continue
                    
                    # Gün metnini hazırla
                    day_text = str(day)
                    
                    # Renk ve stil belirle
                    bg_color = "white"
                    fg_color = "black"
                    font_weight = "normal"
                    
                    if current_day == today:
                        bg_color = "lightblue"
                        font_weight = "bold"
                    
                    if current_day in petition_dates:
                        events = petition_dates[current_day]
                        if any(event[2] == 'red' for event in events):
                            bg_color = "#ffcccb"  # Açık kırmızı
                        elif any(event[2] == 'orange' for event in events):
                            bg_color = "#ffd4a3"  # Açık turuncu
                        elif any(event[2] == 'blue' for event in events):
                            bg_color = "#add8e6"  # Açık mavi
                        
                        day_text += f"\n({len(events)})"
                    
                    button = tk.Button(
                        self.calendar_frame,
                        text=day_text,
                        font=("Arial", 9, font_weight),
                        bg=bg_color,
                        fg=fg_color,
                        relief=tk.RAISED,
                        borderwidth=1,
                        command=lambda d=current_day: self.show_day_info(d)
                    )
                
                button.grid(row=week_num + 1, column=day_num, sticky="nsew", padx=1, pady=1)
                self.day_buttons.append(button)
    
    def show_day_info(self, selected_date):
        """Seçili günün bilgilerini göster"""
        self.info_text.delete(1.0, tk.END)
        
        # Tarih başlığı
        date_str = selected_date.strftime("%d.%m.%Y")
        self.info_text.insert(tk.END, f"📅 {date_str}\n")
        self.info_text.insert(tk.END, "=" * 30 + "\n")
        
        # Dilekçe verilerini kontrol et
        petitions = self.db.get_all_petitions()
        found_events = []
        
        for petition in petitions:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition
            
            # Tarihleri kontrol et
            tebligat_dt = datetime.strptime(tebligat_tarihi, "%Y-%m-%d").date()
            sunum_dt = datetime.strptime(sunum_tarihi, "%Y-%m-%d").date()
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            
            if tebligat_dt == selected_date:
                found_events.append(f"📨 Tebligat: {karar_no}")
            
            if sunum_dt == selected_date:
                found_events.append(f"👔 Avukata Sunum: {karar_no}")
            
            if teslim_dt == selected_date:
                found_events.append(f"⚠️ Son Teslim: {karar_no}")
        
        if found_events:
            for event in found_events:
                self.info_text.insert(tk.END, event + "\n")
        else:
            self.info_text.insert(tk.END, "Bu tarihte hiç etkinlik yok.\n")
        
        # Bugünse ek bilgi
        if selected_date == datetime.now().date():
            self.info_text.insert(tk.END, "\n🎯 BUGÜN\n")
    
    def refresh(self):
        """Takvimi yenile"""
        self.load_calendar_data()