#!/bin/bash

echo "Tebligat Takip Sistemi Kurulum Scripti"
echo "======================================"

# Python kontrolü
echo "Python kontrolü yapılıyor..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python 3.8+ yükleyin."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION bulundu"

# Pip kontrolü ve kurulumu
echo "Pip kontrolü yapılıyor..."
if ! python3 -m pip --version &> /dev/null; then
    echo "⚠️  Pip bulunamadı. Yükleniyor..."
    
    # Ubuntu/Debian için
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip python3-tk
    # CentOS/RHEL için
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip tkinter
    # Fedora için
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip python3-tkinter
    else
        echo "❌ Pip otomatik olarak yüklenemedi. Lütfen manuel olarak yükleyin."
        echo "Daha fazla bilgi için: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
fi

echo "✅ Pip hazır"

# Gerekli paketleri yükle
echo "Gerekli Python paketleri yükleniyor..."
python3 -m pip install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Tüm paketler başarıyla yüklendi"
else
    echo "❌ Paket yükleme hatası!"
    exit 1
fi

# Çalıştırma scriptini oluştur
echo "Çalıştırma scripti oluşturuluyor..."
cat > tebligat-takip.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 src/main.py
EOF

chmod +x tebligat-takip.sh

# Test scriptini çalıştırılabilir yap
chmod +x run_tests.py

echo ""
echo "🎉 Kurulum tamamlandı!"
echo ""
echo "Uygulamayı çalıştırmak için:"
echo "  ./tebligat-takip.sh"
echo ""
echo "Testleri çalıştırmak için:"
echo "  python3 run_tests.py"
echo ""
echo "Manuel çalıştırma için:"
echo "  cd src && python3 main.py"