#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Windows sürümü - hiç locale kullanmaz
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime, timedelta
import threading
import time
from database import Database
from petition_dialog_windows import PetitionDialog
from notification_manager_simple import NotificationManager
from calendar_view import CalendarView

class TebligatTakipApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tebligat Takip Sistemi")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Windows'ta ikonları ayarla
        try:
            self.root.iconbitmap(default="assets/icon.ico")
        except:
            pass
        
        self.db = Database()
        self.notification_manager = NotificationManager(self.db)
        
        self.setup_ui()
        self.load_petitions()
        self.start_notification_timer()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana notebook (sekmeli yapı)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Liste sekmesi
        self.list_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.list_frame, text="📋 Dilekçe Listesi")
        
        # Takvim sekmesi
        self.calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calendar_frame, text="📅 Takvim Görünümü")
        
        # Liste sekmesi içeriği
        self.setup_list_tab()
        
        # Takvim sekmesi içeriği
        self.setup_calendar_tab()
    
    def setup_list_tab(self):
        """Liste sekmesini oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.list_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Başlık
        title_label = ttk.Label(
            main_frame, 
            text="Tebligat Takip Sistemi", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Buton çerçevesi
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Yeni dilekçe ekle butonu
        add_button = ttk.Button(
            button_frame,
            text="+ Yeni Dilekçe Ekle",
            command=self.add_petition,
            width=20
        )
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Yenile butonu
        refresh_button = ttk.Button(
            button_frame,
            text="Yenile",
            command=self.load_petitions,
            width=15
        )
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Arama kutusu
        search_frame = ttk.Frame(button_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Arama:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_petitions)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT)
        
        # Tablo çerçevesi
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tablo
        columns = ("ID", "Karar No", "Dosya No", "Tebligat", "Yasal Süre", 
                  "Avukata Sunum", "Son Teslim", "Kalan Gün")
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show='headings',
            height=15
        )
        
        # Kolon başlıkları
        self.tree.heading("ID", text="ID")
        self.tree.heading("Karar No", text="Karar No")
        self.tree.heading("Dosya No", text="Dosya No")
        self.tree.heading("Tebligat", text="Tebligat Tarihi")
        self.tree.heading("Yasal Süre", text="Yasal Süre (Gün)")
        self.tree.heading("Avukata Sunum", text="Avukata Sunum")
        self.tree.heading("Son Teslim", text="Son Teslim")
        self.tree.heading("Kalan Gün", text="Kalan Gün")
        
        # Kolon genişlikleri
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Karar No", width=140, minwidth=120)
        self.tree.column("Dosya No", width=140, minwidth=120)
        self.tree.column("Tebligat", width=120, minwidth=100)
        self.tree.column("Yasal Süre", width=100, minwidth=80)
        self.tree.column("Avukata Sunum", width=120, minwidth=100)
        self.tree.column("Son Teslim", width=120, minwidth=100)
        self.tree.column("Kalan Gün", width=100, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Tablo ve scrollbar yerleştirme
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # İşlem butonları paneli
        action_frame = ttk.LabelFrame(main_frame, text="İşlemler")
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # İşlem butonları
        ttk.Button(
            action_frame,
            text="✏️ Düzenle",
            command=self.edit_petition,
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            action_frame,
            text="📁 Arşivle",
            command=self.archive_petition,
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            action_frame,
            text="🗑️ Sil",
            command=self.delete_petition,
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            action_frame,
            text="📊 Detaylar",
            command=self.show_details,
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Çift tıklama olayı
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        # Seçim değişikliği olayı
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Sağ tık menüsü
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Düzenle", command=self.edit_petition)
        self.context_menu.add_command(label="Arşivle", command=self.archive_petition)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Sil", command=self.delete_petition)
        
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def setup_calendar_tab(self):
        """Takvim sekmesini oluştur"""
        self.calendar_view = CalendarView(self.calendar_frame, self.db)
        self.calendar_view.pack(fill=tk.BOTH, expand=True)
    
    def load_petitions(self):
        """Dilekçeleri yükle ve tabloya ekle"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        petitions = self.db.get_all_petitions()
        today = datetime.now().date()
        
        for petition in petitions:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition
            
            # Kalan günleri hesapla
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            kalan_gun = (teslim_dt - today).days
            
            # Renk kodlaması için tag belirle
            if kalan_gun < 0:
                tag = "geciken"
            elif kalan_gun <= 2:
                tag = "kritik"
            elif kalan_gun <= 7:
                tag = "yaklasan"
            else:
                tag = "normal"
            
            # Tabloya ekle
            item_id = self.tree.insert('', 'end', values=(
                id_val, karar_no, dosya_no or "-", 
                self.format_date(tebligat_tarihi),
                yasal_sure,
                self.format_date(sunum_tarihi),
                self.format_date(teslim_tarihi),
                kalan_gun
            ), tags=(tag,))
        
        # Renk kodlaması
        self.tree.tag_configure("geciken", background="#ffebee", foreground="#d32f2f")
        self.tree.tag_configure("kritik", background="#fff3e0", foreground="#f57c00")
        self.tree.tag_configure("yaklasan", background="#f3e5f5", foreground="#7b1fa2")
        self.tree.tag_configure("normal", background="white", foreground="black")
        
        self.status_var.set(f"Toplam {len(petitions)} aktif dilekçe")
        
        # Takvimi de güncelle
        if hasattr(self, 'calendar_view'):
            self.calendar_view.refresh()
    
    def filter_petitions(self, *args):
        """Arama filtresini uygula"""
        search_term = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            # Karar no ve dosya no'da ara
            if (search_term in str(values[1]).lower() or 
                search_term in str(values[2]).lower()):
                self.tree.item(item, tags=self.tree.item(item)['tags'])
            else:
                # Gizlemek için farklı bir tag kullan
                current_tags = list(self.tree.item(item)['tags'])
                if 'hidden' not in current_tags:
                    current_tags.append('hidden')
                self.tree.item(item, tags=current_tags)
        
        # Gizli öğeler için stil
        self.tree.tag_configure("hidden", foreground="lightgray")
    
    def format_date(self, date_str):
        """Tarihi güzel formatta göster"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d.%m.%Y")
        except:
            return date_str
    
    def add_petition(self):
        """Yeni dilekçe ekle"""
        dialog = PetitionDialog(self.root, "Yeni Dilekçe Ekle")
        result = dialog.show()
        
        if result:
            try:
                self.db.add_petition(**result)
                self.load_petitions()
                messagebox.showinfo("Başarılı", "Dilekçe başarıyla eklendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dilekçe eklenirken hata oluştu: {str(e)}")
    
    def edit_petition(self):
        """Seçili dilekçeyi düzenle"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek istediğiniz dilekçeyi seçin.")
            return
        
        item = self.tree.item(selected[0])
        petition_id = item['values'][0]
        
        petition_data = self.db.get_petition_by_id(petition_id)
        if petition_data:
            dialog = PetitionDialog(self.root, "Dilekçe Düzenle", petition_data)
            result = dialog.show()
            
            if result:
                try:
                    self.db.update_petition(petition_id, **result)
                    self.load_petitions()
                    messagebox.showinfo("Başarılı", "Dilekçe başarıyla güncellendi!")
                except Exception as e:
                    messagebox.showerror("Hata", f"Dilekçe güncellenirken hata oluştu: {str(e)}")
    
    def archive_petition(self):
        """Seçili dilekçeyi arşivle"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen arşivlemek istediğiniz dilekçeyi seçin.")
            return
        
        if messagebox.askyesno("Onay", "Seçili dilekçeyi arşivlemek istediğinizden emin misiniz?"):
            item = self.tree.item(selected[0])
            petition_id = item['values'][0]
            
            try:
                self.db.archive_petition(petition_id)
                self.load_petitions()
                messagebox.showinfo("Başarılı", "Dilekçe başarıyla arşivlendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dilekçe arşivlenirken hata oluştu: {str(e)}")
    
    def delete_petition(self):
        """Seçili dilekçeyi sil"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz dilekçeyi seçin.")
            return
        
        if messagebox.askyesno("Onay", "Seçili dilekçeyi kalıcı olarak silmek istediğinizden emin misiniz?\nBu işlem geri alınamaz!"):
            item = self.tree.item(selected[0])
            petition_id = item['values'][0]
            
            try:
                self.db.delete_petition(petition_id)
                self.load_petitions()
                messagebox.showinfo("Başarılı", "Dilekçe başarıyla silindi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dilekçe silinirken hata oluştu: {str(e)}")
    
    def on_item_double_click(self, event):
        """Çift tıklama olayı"""
        self.edit_petition()
    
    def on_selection_change(self, event):
        """Seçim değişikliği olayı"""
        # Bu metot gelecekte ek özellikler için kullanılabilir
        pass
    
    def show_details(self):
        """Seçili dilekçenin detaylarını göster"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen detaylarını görmek istediğiniz dilekçeyi seçin.")
            return
        
        item = self.tree.item(selected[0])
        petition_id = item['values'][0]
        
        petition_data = self.db.get_petition_by_id(petition_id)
        if petition_data:
            id_val, karar_no, dosya_no, tebligat_tarihi, yasal_sure, notlar, sunum_tarihi, teslim_tarihi, durum = petition_data
            
            # Detay penceresi
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Dilekçe Detayları - {karar_no}")
            detail_window.geometry("500x400")
            detail_window.resizable(False, False)
            detail_window.transient(self.root)
            detail_window.grab_set()
            
            # İçerik
            frame = ttk.Frame(detail_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Başlık
            ttk.Label(frame, text=f"📋 {karar_no}", font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            # Bilgiler
            info_text = tk.Text(frame, wrap=tk.WORD, height=15, font=("Arial", 10))
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=info_text.yview)
            info_text.configure(yscrollcommand=scrollbar.set)
            
            # İçerik hazırla
            today = datetime.now().date()
            teslim_dt = datetime.strptime(teslim_tarihi, "%Y-%m-%d").date()
            kalan_gun = (teslim_dt - today).days
            
            durum_rengi = "🔴" if kalan_gun < 0 else "🟠" if kalan_gun <= 2 else "🟣" if kalan_gun <= 7 else "🟢"
            
            content = f"""
{durum_rengi} GENEL BİLGİLER
═══════════════════════════════════════

📁 Karar Numarası: {karar_no}
📂 Dosya Numarası: {dosya_no or 'Belirtilmemiş'}
📅 Tebligat Tarihi: {self.format_date(tebligat_tarihi)}
⏱️ Yasal Süre: {yasal_sure} gün
📊 Durum: {durum.upper()}

⏰ TARİH BİLGİLERİ
═══════════════════════════════════════

👔 Avukata Sunum: {self.format_date(sunum_tarihi)}
⚠️ Son Teslim: {self.format_date(teslim_tarihi)}
📊 Kalan Gün: {kalan_gun}

📝 NOTLAR
═══════════════════════════════════════

{notlar if notlar else 'Not bulunmuyor.'}

💡 DURUM DEĞERLENDİRMESİ
═══════════════════════════════════════

"""
            
            if kalan_gun < 0:
                content += f"🚨 DİKKAT: Bu dilekçe {abs(kalan_gun)} gün gecikmiş!\nAcil işlem gerekli!"
            elif kalan_gun == 0:
                content += "⚠️ BUGÜN son teslim tarihi!"
            elif kalan_gun <= 2:
                content += f"🔥 Kritik: Sadece {kalan_gun} gün kaldı!"
            elif kalan_gun <= 7:
                content += f"⚡ Yaklaşan: {kalan_gun} gün kaldı."
            else:
                content += f"✅ Normal: {kalan_gun} gün var."
            
            info_text.insert(tk.END, content)
            info_text.config(state=tk.DISABLED)
            
            info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Kapat butonu
            ttk.Button(
                frame,
                text="Kapat",
                command=detail_window.destroy,
                width=15
            ).pack(pady=(10, 0))
    
    def show_context_menu(self, event):
        """Sağ tık menüsünü göster"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def start_notification_timer(self):
        """Bildirim zamanlayıcısını başlat"""
        def check_notifications():
            while True:
                try:
                    self.notification_manager.check_and_send_notifications()
                except Exception as e:
                    print(f"Bildirim hatası: {e}")
                time.sleep(3600)  # Her saat kontrol et
        
        notification_thread = threading.Thread(target=check_notifications, daemon=True)
        notification_thread.start()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

def main():
    print("Basit Windows sürümü başlatılıyor...")
    app = TebligatTakipApp()
    app.run()

if __name__ == "__main__":
    main()