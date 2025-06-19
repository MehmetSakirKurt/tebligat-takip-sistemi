# Windows Kurulum Kılavuzu

## Hızlı Başlangıç

### 1. Uygulamayı Çalıştırma
```cmd
# Çift tıklama ile
run_windows.bat

# Veya komut satırından
python run_windows.py
```

### 2. Eğer Hata Alırsanız
```cmd
# Python versiyonunu kontrol edin
python --version

# Gerekli paketleri yükleyin (isteğe bağlı)
pip install ttkbootstrap tkcalendar plyer
```

## Detaylı Kurulum

### Gereksinimler
- ✅ **Python 3.8+** (zorunlu)
- ✅ **tkinter** (genellikle Python ile gelir)
- ⚠️ **ttkbootstrap** (isteğe bağlı - daha güzel arayüz için)
- ⚠️ **tkcalendar** (isteğe bağlı - takvim widget'ı için)
- ⚠️ **plyer** (isteğe bağlı - masaüstü bildirimleri için)

### Adım Adım Kurulum

#### 1. Python Kurulumu
```cmd
# Python yüklü mü kontrol edin
python --version
```

Eğer Python yüklü değilse:
1. https://www.python.org/downloads/ adresinden indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın

#### 2. Temel Çalıştırma
```cmd
# Temel sürümü çalıştırın (sadece tkinter ile)
python run_windows.py
```

#### 3. Gelişmiş Özellikler (İsteğe Bağlı)
```cmd
# Daha güzel arayüz için
pip install ttkbootstrap

# Takvim widget'ı için
pip install tkcalendar

# Masaüstü bildirimleri için
pip install plyer

# Hepsini birden
pip install ttkbootstrap tkcalendar plyer
```

## Sorun Giderme

### "python komutu tanınmıyor" Hatası
1. Python'un PATH'e eklendiğinden emin olun
2. Komut istemcisini yeniden başlatın
3. `py` komutunu deneyin: `py run_windows.py`

### "No module named 'tkinter'" Hatası
```cmd
# Windows'ta tkinter genellikle varsayılan gelir
# Eğer yoksa Python'u yeniden kurun

# Alternatif olarak:
pip install tk
```

### Locale/Dil Hatası
Bu uygulama Windows locale sorunlarını otomatik çözer. Hiçbir şey yapmanıza gerek yok.

### Bildirimler Çalışmıyor
```cmd
# Plyer paketini yükleyin
pip install plyer

# Windows bildirim izinlerini kontrol edin
# Ayarlar > Sistem > Bildirimler
```

## Kullanım

### Temel İşlemler
1. **Yeni Dilekçe**: "Yeni Dilekçe Ekle" butonuna tıklayın
2. **Düzenleme**: Satıra çift tıklayın veya sağ tık > "Düzenle"
3. **Arşivleme**: Sağ tık > "Arşivle"
4. **Silme**: Sağ tık > "Sil" (dikkatli olun!)

### Tarih Seçimi
- Windows sürümünde basit tarih seçici kullanılır
- Gün/Ay/Yıl alanlarını elle girin veya ok tuşlarını kullanın

### Renk Kodları
- 🔴 **Kırmızı**: Süresi geçmiş
- 🟠 **Turuncu**: 2 gün veya daha az kalmış
- 🔵 **Mavi**: 3-7 gün kalmış
- 🟢 **Yeşil**: Normal durumda

## Performans İpuçları

1. **Hızlı Başlatma**: `run_windows.bat` dosyasını masaüstüne kopyalayın
2. **Otomatik Başlatma**: Windows başlangıç klasörüne kısayol ekleyin
3. **Yedekleme**: `tebligat.db` dosyasını düzenli olarak yedekleyin

## Güncelleme

Yeni sürüm için:
1. Eski klasörü yedekleyin
2. Yeni dosyaları indirin
3. `tebligat.db` dosyasını yeni klasöre kopyalayın

---

**Destek**: Sorun yaşarsanız `run_windows.py` dosyasını komut satırından çalıştırıp hata mesajlarını kontrol edin.