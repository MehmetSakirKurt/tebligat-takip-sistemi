#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Windows için basit tarih seçici
class SimpleDatePicker:
    def __init__(self, parent):
        self.parent = parent
        self.date = datetime.now().date()
        
        self.frame = ttk.Frame(parent)
        
        # Gün
        ttk.Label(self.frame, text="Gün:").grid(row=0, column=0, padx=2)
        self.day_var = tk.StringVar(value=str(self.date.day))
        day_spin = ttk.Spinbox(self.frame, from_=1, to=31, textvariable=self.day_var, width=5)
        day_spin.grid(row=0, column=1, padx=2)
        
        # Ay
        ttk.Label(self.frame, text="Ay:").grid(row=0, column=2, padx=2)
        self.month_var = tk.StringVar(value=str(self.date.month))
        month_spin = ttk.Spinbox(self.frame, from_=1, to=12, textvariable=self.month_var, width=5)
        month_spin.grid(row=0, column=3, padx=2)
        
        # Yıl
        ttk.Label(self.frame, text="Yıl:").grid(row=0, column=4, padx=2)
        self.year_var = tk.StringVar(value=str(self.date.year))
        year_spin = ttk.Spinbox(self.frame, from_=2020, to=2030, textvariable=self.year_var, width=8)
        year_spin.grid(row=0, column=5, padx=2)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def get_date(self):
        try:
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            return datetime(year, month, day).date()
        except:
            return datetime.now().date()
    
    def set_date(self, date):
        self.day_var.set(str(date.day))
        self.month_var.set(str(date.month))
        self.year_var.set(str(date.year))

class PetitionDialog:
    def __init__(self, parent, title, petition_data=None):
        self.parent = parent
        self.title = title
        self.petition_data = petition_data
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Dialog'u ekranın ortasına yerleştir
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        self.populate_fields()
        
    def setup_ui(self):
        """Dialog UI'ını oluştur"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = ttk.Label(
            main_frame,
            text=self.title,
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Form alanları
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Karar Numarası
        karar_frame = ttk.Frame(fields_frame)
        karar_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            karar_frame,
            text="Karar Numarası *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.karar_no_var = tk.StringVar()
        karar_entry = ttk.Entry(
            karar_frame,
            textvariable=self.karar_no_var,
            font=("Arial", 10)
        )
        karar_entry.pack(fill=tk.X, pady=(5, 0))
        karar_entry.focus()
        
        # Dosya Numarası
        dosya_frame = ttk.Frame(fields_frame)
        dosya_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            dosya_frame,
            text="Dosya Numarası",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.dosya_no_var = tk.StringVar()
        dosya_entry = ttk.Entry(
            dosya_frame,
            textvariable=self.dosya_no_var,
            font=("Arial", 10)
        )
        dosya_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Tebligat Tarihi
        tebligat_frame = ttk.Frame(fields_frame)
        tebligat_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            tebligat_frame,
            text="Tebligat Tarihi *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.tebligat_tarihi = SimpleDatePicker(tebligat_frame)
        self.tebligat_tarihi.pack(fill=tk.X, pady=(5, 0))
        
        # Yasal Süre
        sure_frame = ttk.Frame(fields_frame)
        sure_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            sure_frame,
            text="Yasal Süre (Gün) *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.yasal_sure_var = tk.StringVar(value="30")
        sure_spinbox = ttk.Spinbox(
            sure_frame,
            from_=1,
            to=365,
            textvariable=self.yasal_sure_var,
            font=("Arial", 10),
            command=self.calculate_dates
        )
        sure_spinbox.pack(fill=tk.X, pady=(5, 0))
        sure_spinbox.bind('<KeyRelease>', self.calculate_dates)
        
        # Hesaplanan Tarihler Bölümü
        calc_frame = ttk.LabelFrame(
            fields_frame,
            text="Hesaplanan Tarihler",
            padding=10
        )
        calc_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Avukata Sunum Tarihi
        sunum_info_frame = ttk.Frame(calc_frame)
        sunum_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            sunum_info_frame,
            text="Avukata Sunum Tarihi:",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)
        
        self.sunum_tarihi_label = ttk.Label(
            sunum_info_frame,
            text="-",
            font=("Arial", 10),
            foreground="green"
        )
        self.sunum_tarihi_label.pack(side=tk.RIGHT)
        
        # Son Teslim Tarihi
        teslim_info_frame = ttk.Frame(calc_frame)
        teslim_info_frame.pack(fill=tk.X)
        
        ttk.Label(
            teslim_info_frame,
            text="Son Teslim Tarihi:",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)
        
        self.teslim_tarihi_label = ttk.Label(
            teslim_info_frame,
            text="-",
            font=("Arial", 10),
            foreground="green"
        )
        self.teslim_tarihi_label.pack(side=tk.RIGHT)
        
        # Notlar
        notlar_frame = ttk.Frame(fields_frame)
        notlar_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        ttk.Label(
            notlar_frame,
            text="Notlar",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        # Text widget için frame
        text_frame = ttk.Frame(notlar_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.notlar_text = tk.Text(
            text_frame,
            height=4,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.notlar_text.yview)
        self.notlar_text.configure(yscrollcommand=scrollbar.set)
        
        self.notlar_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # İptal butonu
        cancel_button = ttk.Button(
            button_frame,
            text="İptal",
            command=self.cancel,
            width=15
        )
        cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Kaydet butonu
        save_button = ttk.Button(
            button_frame,
            text="Kaydet",
            command=self.save,
            width=15
        )
        save_button.pack(side=tk.RIGHT)
        
        # Enter ve Escape tuşu bağlamaları
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # İlk hesaplamayı yap
        self.calculate_dates()
    
    def populate_fields(self):
        """Mevcut petition verilerini alanlara doldur"""
        if self.petition_data:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = self.petition_data
            
            self.karar_no_var.set(karar_no)
            self.dosya_no_var.set(dosya_no or "")
            
            # Tebligat tarihini ayarla
            tebligat_dt = datetime.strptime(tebligat_tarihi, "%Y-%m-%d")
            self.tebligat_tarihi.set_date(tebligat_dt.date())
            
            self.yasal_sure_var.set(str(yasal_sure))
            
            # Notları doldur
            self.notlar_text.delete(1.0, tk.END)
            if notlar:
                self.notlar_text.insert(1.0, notlar)
            
            # Tarihleri hesapla
            self.calculate_dates()
    
    def calculate_dates(self, event=None):
        """Avukata sunum ve son teslim tarihlerini hesapla"""
        try:
            tebligat_tarihi = self.tebligat_tarihi.get_date()
            yasal_sure = int(self.yasal_sure_var.get() or 0)
            
            if yasal_sure > 0:
                # Son teslim tarihi
                teslim_tarihi = tebligat_tarihi + timedelta(days=yasal_sure)
                # Avukata sunum tarihi (2 gün önce)
                sunum_tarihi = teslim_tarihi - timedelta(days=2)
                
                self.sunum_tarihi_label.config(text=sunum_tarihi.strftime("%d.%m.%Y"))
                self.teslim_tarihi_label.config(text=teslim_tarihi.strftime("%d.%m.%Y"))
                
                # Tarihlerin rengini belirle
                today = datetime.now().date()
                days_until_deadline = (teslim_tarihi - today).days
                
                if days_until_deadline < 0:
                    color = "red"
                elif days_until_deadline <= 2:
                    color = "orange"
                elif days_until_deadline <= 7:
                    color = "blue"
                else:
                    color = "green"
                
                self.sunum_tarihi_label.config(foreground=color)
                self.teslim_tarihi_label.config(foreground=color)
            else:
                self.sunum_tarihi_label.config(text="-")
                self.teslim_tarihi_label.config(text="-")
                
        except (ValueError, TypeError):
            self.sunum_tarihi_label.config(text="-")
            self.teslim_tarihi_label.config(text="-")
    
    def validate_form(self):
        """Form verilerini doğrula"""
        if not self.karar_no_var.get().strip():
            messagebox.showerror("Hata", "Karar numarası zorunludur!")
            return False
        
        try:
            yasal_sure = int(self.yasal_sure_var.get())
            if yasal_sure <= 0:
                messagebox.showerror("Hata", "Yasal süre pozitif bir sayı olmalıdır!")
                return False
        except ValueError:
            messagebox.showerror("Hata", "Yasal süre geçerli bir sayı olmalıdır!")
            return False
        
        return True
    
    def save(self):
        """Formu kaydet"""
        if not self.validate_form():
            return
        
        try:
            self.result = {
                'karar_no': self.karar_no_var.get().strip(),
                'dosya_no': self.dosya_no_var.get().strip(),
                'tebligat_tarihi': self.tebligat_tarihi.get_date().strftime("%Y-%m-%d"),
                'yasal_sure': int(self.yasal_sure_var.get()),
                'notlar': self.notlar_text.get(1.0, tk.END).strip()
            }
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Form kaydedilirken hata oluştu: {str(e)}")
    
    def cancel(self):
        """Dialog'u iptal et"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Dialog'u göster ve sonucu döndür"""
        self.dialog.wait_window()
        return self.result