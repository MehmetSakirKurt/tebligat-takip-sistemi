# Tebligat Takip Sistemi - Kullanım Kılavuzu

## Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- Tkinter (genellikle Python ile birlikte gelir)
- İnternet bağlantısı (ilk kurulum için)

### Otomatik Kurulum (Önerilen)

```bash
# Kurulum scriptini çalıştır
./install.sh
```

### Manuel Kurulum

```bash
# Gerekli paketleri yükle
pip3 install --user -r requirements.txt

# Uygulamayı çalıştır
cd src
python3 main.py
```

## Uygulamayı Çalıştırma

### Otomatik Script ile
```bash
./tebligat-takip.sh
```

### Manuel Çalıştırma
```bash
cd src
python3 main.py
```

## Özellikler ve Kullanım

### 1. Yeni Dilekçe Ekleme
- Ana ekranda **"➕ Yeni Dilekçe Ekle"** butonuna tıklayın
- Zorunlu alanları doldurun:
  - **Karar Numarası**: Mahkeme kararının numarası
  - **Tebligat Tarihi**: Tebligat alındığı tarih (takvimden seçin)
  - **Yasal Süre**: Gün cinsinden süre (varsayılan 30 gün)
- İsterseniz doldurun:
  - **Dosya Numarası**: İçsel takip numarası
  - **Notlar**: Ek açıklamalar
- **Kaydet** butonuna tıklayın

### 2. Otomatik Tarih Hesaplama
Sistem otomatik olarak hesaplar:
- **Avukata Sunum Tarihi**: Son teslim tarihinden 2 gün önce
- **Son Teslim Tarihi**: Tebligat tarihi + yasal süre

### 3. Dilekçe Yönetimi

#### Düzenleme
- İstediğiniz satıra **çift tıklayın** VEYA
- Satıra **sağ tıklayıp** "Düzenle" seçin

#### Arşivleme
- Satıra **sağ tıklayıp** "Arşivle" seçin
- Arşivlenen dilekçeler listeden kaldırılır ama silinmez

#### Silme
- Satıra **sağ tıklayıp** "Sil" seçin
- **DİKKAT**: Bu işlem geri alınamaz!

### 4. Arama ve Filtreleme
- Sağ üst köşedeki **Arama** kutusunu kullanın
- Karar numarası veya dosya numarasında arama yapar

### 5. Renk Kodları
- 🔴 **Kırmızı**: Süresi geçmiş dilekçeler
- 🟠 **Turuncu**: 2 gün veya daha az kalmış (kritik)
- 🟣 **Mor**: 3-7 gün kalmış (yaklaşan)
- ⚪ **Beyaz**: Normal durumda olanlar

### 6. Masaüstü Bildirimleri
Sistem otomatik olarak bildirim gönderir:
- **Avukata Sunum Günü**: Sunum tarihi geldiğinde
- **Son Teslim Uyarısı**: Son teslim tarihinden 1 gün önce
- **Son Teslim Günü**: Son teslim tarihi geldiğinde
- **Gecikme Uyarısı**: Süre geçtikten sonra her gün

## Dosya Konumları

- **Veritabanı**: `tebligat.db` (uygulama dizininde)
- **Bildirim Geçmişi**: `notification_history.json`
- **Loglar**: Konsol çıktısında

## Sorun Giderme

### Uygulama Açılmıyor
```bash
# Python versiyonunu kontrol edin
python3 --version

# Gerekli paketleri tekrar yükleyin
pip3 install --user -r requirements.txt

# Manuel çalıştırmayı deneyin
cd src
python3 main.py
```

### Bildirimler Çalışmıyor
- Linux sistemlerde: `libnotify-dev` paketini yükleyin
- Windows sistemlerde: Genellikle otomatik çalışır
- macOS sistemlerde: Sistem bildirimlerine izin verin

### Veritabanı Sorunları
Veritabanı bozulursa:
```bash
# Veritabanı dosyasını silin (veriler kaybolur!)
rm tebligat.db

# Uygulamayı yeniden başlatın
./tebligat-takip.sh
```

## Yedekleme

### Verileri Yedekleme
```bash
# Veritabanını kopyalayın
cp tebligat.db tebligat_backup_$(date +%Y%m%d).db
```

### Yedekten Geri Yükleme
```bash
# Yedek dosyasını ana dosya olarak kopyalayın
cp tebligat_backup_YYYYMMDD.db tebligat.db
```

## İpuçları

1. **Düzenli Yedekleme**: Önemli veriler için düzenli yedek alın
2. **Bildirim Testı**: İlk kurulumda bir test dilekçesi ekleyerek bildirimleri test edin
3. **Toplu İşlem**: Çok sayıda dilekçe için Excel'den verileri kopyala-yapıştır yapın
4. **Ekran Çözünürlüğü**: 1024x768 veya daha büyük çözünürlük önerilir

## Destek

Sorun yaşadığınızda:
1. Bu kılavuzu tekrar okuyun
2. Terminal/komut istemcisinden çalıştırıp hata mesajlarını kontrol edin
3. Python versiyonu ve paket sürümlerini kontrol edin

---
**Not**: Bu uygulama offline çalışır ve verileriniz sadece bilgisayarınızda saklanır.