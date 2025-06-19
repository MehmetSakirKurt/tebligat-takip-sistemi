import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from tkcalendar import DateEntry
from datetime import datetime, timedelta

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
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Başlık
        title_label = ttk_bs.Label(
            main_frame,
            text=self.title,
            font=("Arial", 14, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Form alanları
        fields_frame = ttk_bs.Frame(main_frame)
        fields_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        # Karar Numarası
        karar_frame = ttk_bs.Frame(fields_frame)
        karar_frame.pack(fill=X, pady=(0, 15))
        
        ttk_bs.Label(
            karar_frame,
            text="Karar Numarası *",
            font=("Arial", 10, "bold")
        ).pack(anchor=W)
        
        self.karar_no_var = tk.StringVar()
        karar_entry = ttk_bs.Entry(
            karar_frame,
            textvariable=self.karar_no_var,
            font=("Arial", 10),
            bootstyle=INFO
        )
        karar_entry.pack(fill=X, pady=(5, 0))
        karar_entry.focus()
        
        # Dosya Numarası
        dosya_frame = ttk_bs.Frame(fields_frame)
        dosya_frame.pack(fill=X, pady=(0, 15))
        
        ttk_bs.Label(
            dosya_frame,
            text="Dosya Numarası",
            font=("Arial", 10, "bold")
        ).pack(anchor=W)
        
        self.dosya_no_var = tk.StringVar()
        dosya_entry = ttk_bs.Entry(
            dosya_frame,
            textvariable=self.dosya_no_var,
            font=("Arial", 10),
            bootstyle=INFO
        )
        dosya_entry.pack(fill=X, pady=(5, 0))
        
        # Tebligat Tarihi
        tebligat_frame = ttk_bs.Frame(fields_frame)
        tebligat_frame.pack(fill=X, pady=(0, 15))
        
        ttk_bs.Label(
            tebligat_frame,
            text="Tebligat Tarihi *",
            font=("Arial", 10, "bold")
        ).pack(anchor=W)
        
        self.tebligat_tarihi = DateEntry(
            tebligat_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd.mm.yyyy',
            font=("Arial", 10)
        )
        self.tebligat_tarihi.pack(fill=X, pady=(5, 0))
        self.tebligat_tarihi.bind('<<DateEntrySelected>>', self.calculate_dates)
        
        # Yasal Süre
        sure_frame = ttk_bs.Frame(fields_frame)
        sure_frame.pack(fill=X, pady=(0, 15))
        
        ttk_bs.Label(
            sure_frame,
            text="Yasal Süre (Gün) *",
            font=("Arial", 10, "bold")
        ).pack(anchor=W)
        
        self.yasal_sure_var = tk.StringVar(value="30")
        sure_spinbox = ttk_bs.Spinbox(
            sure_frame,
            from_=1,
            to=365,
            textvariable=self.yasal_sure_var,
            font=("Arial", 10),
            bootstyle=INFO,
            command=self.calculate_dates
        )
        sure_spinbox.pack(fill=X, pady=(5, 0))
        sure_spinbox.bind('<KeyRelease>', self.calculate_dates)
        
        # Hesaplanan Tarihler Bölümü
        calc_frame = ttk_bs.LabelFrame(
            fields_frame,
            text="Hesaplanan Tarihler",
            bootstyle=SUCCESS,
            padding=10
        )
        calc_frame.pack(fill=X, pady=(0, 15))
        
        # Avukata Sunum Tarihi
        sunum_info_frame = ttk_bs.Frame(calc_frame)
        sunum_info_frame.pack(fill=X, pady=(0, 10))
        
        ttk_bs.Label(
            sunum_info_frame,
            text="Avukata Sunum Tarihi:",
            font=("Arial", 10, "bold")
        ).pack(side=LEFT)
        
        self.sunum_tarihi_label = ttk_bs.Label(
            sunum_info_frame,
            text="-",
            font=("Arial", 10),
            bootstyle=SUCCESS
        )
        self.sunum_tarihi_label.pack(side=RIGHT)
        
        # Son Teslim Tarihi
        teslim_info_frame = ttk_bs.Frame(calc_frame)
        teslim_info_frame.pack(fill=X)
        
        ttk_bs.Label(
            teslim_info_frame,
            text="Son Teslim Tarihi:",
            font=("Arial", 10, "bold")
        ).pack(side=LEFT)
        
        self.teslim_tarihi_label = ttk_bs.Label(
            teslim_info_frame,
            text="-",
            font=("Arial", 10),
            bootstyle=SUCCESS
        )
        self.teslim_tarihi_label.pack(side=RIGHT)
        
        # Notlar
        notlar_frame = ttk_bs.Frame(fields_frame)
        notlar_frame.pack(fill=BOTH, expand=True, pady=(0, 15))
        
        ttk_bs.Label(
            notlar_frame,
            text="Notlar",
            font=("Arial", 10, "bold")
        ).pack(anchor=W)
        
        # Text widget için frame
        text_frame = ttk_bs.Frame(notlar_frame)
        text_frame.pack(fill=BOTH, expand=True, pady=(5, 0))
        
        self.notlar_text = tk.Text(
            text_frame,
            height=4,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        
        # Scrollbar
        scrollbar = ttk_bs.Scrollbar(text_frame, orient=VERTICAL, command=self.notlar_text.yview)
        self.notlar_text.configure(yscrollcommand=scrollbar.set)
        
        self.notlar_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Butonlar
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X)
        
        # İptal butonu
        cancel_button = ttk_bs.Button(
            button_frame,
            text="İptal",
            bootstyle=SECONDARY,
            command=self.cancel,
            width=15
        )
        cancel_button.pack(side=RIGHT, padx=(10, 0))
        
        # Kaydet butonu
        save_button = ttk_bs.Button(
            button_frame,
            text="Kaydet",
            bootstyle=SUCCESS,
            command=self.save,
            width=15
        )
        save_button.pack(side=RIGHT)
        
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
                    style = DANGER
                elif days_until_deadline <= 2:
                    style = WARNING
                elif days_until_deadline <= 7:
                    style = INFO
                else:
                    style = SUCCESS
                
                self.sunum_tarihi_label.config(bootstyle=style)
                self.teslim_tarihi_label.config(bootstyle=style)
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