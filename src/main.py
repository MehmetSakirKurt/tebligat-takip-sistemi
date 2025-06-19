import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import threading
import time
from database import Database
from petition_dialog import PetitionDialog
from notification_manager import NotificationManager

class TebligatTakipApp:
    def __init__(self):
        self.root = ttk_bs.Window(themename="flatly")
        self.root.title("Tebligat Takip Sistemi")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        self.db = Database()
        self.notification_manager = NotificationManager(self.db)
        
        self.setup_ui()
        self.load_petitions()
        self.start_notification_timer()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana frame
        main_frame = ttk_bs.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Başlık
        title_label = ttk_bs.Label(
            main_frame, 
            text="Tebligat Takip Sistemi", 
            font=("Arial", 18, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Buton çerçevesi
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=(0, 20))
        
        # Yeni dilekçe ekle butonu
        add_button = ttk_bs.Button(
            button_frame,
            text="➕ Yeni Dilekçe Ekle",
            bootstyle=SUCCESS,
            command=self.add_petition,
            width=20
        )
        add_button.pack(side=LEFT, padx=(0, 10))
        
        # Yenile butonu
        refresh_button = ttk_bs.Button(
            button_frame,
            text="🔄 Yenile",
            bootstyle=INFO,
            command=self.load_petitions,
            width=15
        )
        refresh_button.pack(side=LEFT, padx=(0, 10))
        
        # Arama kutusu
        search_frame = ttk_bs.Frame(button_frame)
        search_frame.pack(side=RIGHT)
        
        ttk_bs.Label(search_frame, text="Arama:").pack(side=LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_petitions)
        search_entry = ttk_bs.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=LEFT)
        
        # Tablo çerçevesi
        table_frame = ttk_bs.Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Tablo
        columns = ("ID", "Karar No", "Dosya No", "Tebligat", "Yasal Süre", 
                  "Avukata Sunum", "Son Teslim", "Kalan Gün", "İşlemler")
        
        self.tree = ttk_bs.Treeview(
            table_frame, 
            columns=columns, 
            show='headings',
            height=15,
            bootstyle=INFO
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
        self.tree.heading("İşlemler", text="İşlemler")
        
        # Kolon genişlikleri
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Karar No", width=120, minwidth=100)
        self.tree.column("Dosya No", width=120, minwidth=100)
        self.tree.column("Tebligat", width=100, minwidth=100)
        self.tree.column("Yasal Süre", width=80, minwidth=80)
        self.tree.column("Avukata Sunum", width=100, minwidth=100)
        self.tree.column("Son Teslim", width=100, minwidth=100)
        self.tree.column("Kalan Gün", width=80, minwidth=80)
        self.tree.column("İşlemler", width=150, minwidth=150)
        
        # Scrollbar
        scrollbar = ttk_bs.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Tablo ve scrollbar yerleştirme
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Çift tıklama olayı
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
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
        status_bar = ttk_bs.Label(
            main_frame, 
            textvariable=self.status_var,
            bootstyle=SECONDARY,
            relief=SUNKEN
        )
        status_bar.pack(fill=X, pady=(10, 0))
    
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
                kalan_gun,
                "Düzenle | Arşivle | Sil"
            ), tags=(tag,))
        
        # Renk kodlaması
        self.tree.tag_configure("geciken", background="#ffebee", foreground="#d32f2f")
        self.tree.tag_configure("kritik", background="#fff3e0", foreground="#f57c00")
        self.tree.tag_configure("yaklasan", background="#f3e5f5", foreground="#7b1fa2")
        self.tree.tag_configure("normal", background="white", foreground="black")
        
        self.status_var.set(f"Toplam {len(petitions)} aktif dilekçe")
    
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
                self.notification_manager.check_and_send_notifications()
                time.sleep(3600)  # Her saat kontrol et
        
        notification_thread = threading.Thread(target=check_notifications, daemon=True)
        notification_thread.start()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

def main():
    app = TebligatTakipApp()
    app.run()

if __name__ == "__main__":
    main()