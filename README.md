# Otomatik Mail Gönderme Uygulaması

Bu uygulama, Python kullanarak otomatik mail gönderme işlemlerini gerçekleştiren kapsamlı bir sistemdir. Hem GUI (grafik arayüz) hem de komut satırı desteği sunar.

## Özellikler

- ✅ **Grafik Arayüz (GUI)**: Kolay kullanımlı tkinter tabanlı arayüz
- ✅ **Komut Satırı Desteği**: CLI ile hızlı mail gönderimi
- ✅ **Toplu Mail Gönderimi**: Birden fazla alıcıya aynı anda mail
- ✅ **HTML Mail Desteği**: Zengin içerikli HTML mailler
- ✅ **Ek Dosya Desteği**: Dosya ekleme özelliği
- ✅ **Mail Şablonları**: Hazır mail şablonları
- ✅ **Zamanlayıcı**: Otomatik mail gönderimi planlaması
- ✅ **Kişiselleştirme**: Değişken kullanarak kişisel mailler
- ✅ **Log Sistemi**: Detaylı log kayıtları
- ✅ **Yapılandırma**: Kolay SMTP ayarları

## Kurulum

1. **Python Gereksinimleri**:
   ```bash
   pip install schedule
   ```
   
2. **Dosyaları İndirin**: Tüm `.py` dosyalarını aynı klasöre koyun

3. **SMTP Ayarları**: Gmail, Outlook vb. için SMTP ayarlarını yapılandırın

## Hızlı Başlangıç

### 1. Grafik Arayüzü Başlatma
```bash
python gui.py
```

### 2. Komut Satırı Kullanımı
```bash
python cli.py
```

### 3. Örnekleri İnceleme
```bash
python examples.py
```

## SMTP Yapılandırması

### Gmail için:
- **SMTP Server**: smtp.gmail.com
- **Port**: 587
- **Güvenlik**: 2FA aktifse "App Password" kullanın
- **Ayar**: "Az güvenli uygulamalara izin ver" seçeneğini açın

### Outlook için:
- **SMTP Server**: smtp-mail.outlook.com
- **Port**: 587
- **Güvenlik**: Normal şifre kullanılabilir

## Kullanım Örnekleri

### Tek Mail Gönderimi
```python
from mail_sender import MailSender

mail_sender = MailSender()
success = mail_sender.send_mail(
    to_email='recipient@example.com',
    subject='Test Mail',
    body='Bu bir test mailidir.',
    is_html=False
)
```

### HTML Mail Gönderimi
```python
html_body = """
<html>
<body>
    <h2>Merhaba!</h2>
    <p>Bu bir <b>HTML</b> mail örneğidir.</p>
</body>
</html>
"""

success = mail_sender.send_mail(
    to_email='recipient@example.com',
    subject='HTML Mail',
    body=html_body,
    is_html=True
)
```

### Toplu Mail Gönderimi
```python
recipients = [
    'user1@example.com',
    'user2@example.com',
    'user3@example.com'
]

results = mail_sender.send_bulk_mail(
    recipients=recipients,
    subject='Toplu Mail',
    body='Bu toplu mail gönderim testidir.'
)
```

### Ek Dosyalı Mail
```python
success = mail_sender.send_mail(
    to_email='recipient@example.com',
    subject='Ek Dosyalı Mail',
    body='Bu mail ek dosya içermektedir.',
    attachments=['dosya1.pdf', 'dosya2.jpg']
)
```

### Ek Dosyalı Toplu Mail
```python
recipients = [
    'user1@example.com',
    'user2@example.com',
    'user3@example.com'
]

# Ek dosyalar
attachments = ['dosya1.pdf', 'dosya2.jpg', 'rapor.docx']

results = mail_sender.send_bulk_mail(
    recipients=recipients,
    subject='Ek Dosyalı Toplu Mail',
    body='Bu toplu mail ek dosyalar içermektedir.',
    attachments=attachments,
    is_html=False
)
```

### Şablon Kullanımı
```python
templates = mail_sender.get_mail_templates()
welcome_template = templates['welcome']

body = welcome_template['body'].format(
    name='Ahmet Yılmaz',
    company='ABC Şirketi'
)

success = mail_sender.send_mail(
    to_email='ahmet@example.com',
    subject=welcome_template['subject'],
    body=body
)
```

## Zamanlayıcı Kullanımı

```python
from scheduler import ScheduledMailSender

scheduler = ScheduledMailSender()

# Günlük mail planla
scheduler.schedule_daily_mail(
    time_str='09:00',
    to_email='manager@example.com',
    subject='Günlük Rapor',
    body='Bu günlük rapor mailidir.'
)

# Haftalık mail planla
scheduler.schedule_weekly_mail(
    day='monday',
    time_str='10:00',
    to_email='team@example.com',
    subject='Haftalık Toplantı',
    body='Haftalık toplantı hatırlatması.'
)

# Zamanlayıcıyı başlat
scheduler.start_scheduler()
```

## Dosya Yapısı

```
mail gönderme/
├── mail_sender.py      # Ana mail gönderme sınıfı
├── gui.py             # Grafik arayüz uygulaması
├── cli.py             # Komut satırı uygulaması
├── scheduler.py       # Zamanlayıcı sistemi
├── examples.py        # Kullanım örnekleri
├── requirements.txt   # Python gereksinimleri
├── README.md         # Bu dosya
├── config.json       # SMTP yapılandırması (otomatik oluşur)
└── mail_logs.log     # Log dosyası (otomatik oluşur)
```

## Şablonlar

Uygulama 3 hazır şablon içerir:

1. **welcome**: Hoş geldin maili
2. **reminder**: Hatırlatma maili
3. **newsletter**: HTML newsletter

### Şablon Değişkenleri
- `{name}`: Kişi adı
- `{company}`: Şirket adı
- `{date}`: Tarih
- `{reminder_text}`: Hatırlatma metni
- `{news_item_1}`, `{news_item_2}`, `{news_item_3}`: Haber maddeleri

## Güvenlik Notları

1. **App Password**: Gmail için mutlaka uygulama şifresi kullanın
2. **2FA**: İki faktörlü kimlik doğrulama açın
3. **Şifre Güvenliği**: Şifreleri asla kodda saklamayın
4. **Rate Limiting**: Toplu mail gönderirken hız limitlerini dikkate alın

## Sorun Giderme

### "Authentication failed" Hatası
- Gmail için uygulama şifresi kullanın
- "Az güvenli uygulamalara izin ver" seçeneğini açın
- SMTP ayarlarını kontrol edin

### "Connection refused" Hatası
- İnternet bağlantınızı kontrol edin
- SMTP server ve port ayarlarını doğrulayın
- Firewall ayarlarını kontrol edin

### "Quota exceeded" Hatası
- Gmail günlük gönderim limitini aştınız
- Daha az mail gönderin veya bekleyin

## 📊 **Gmail Limitleri ve Güvenli Gönderim**

### **Gmail Günlük Limitler:**
- **Ücretsiz Gmail**: 500 mail/gün
- **Google Workspace**: 2,000 mail/gün
- **Saatlik limit**: ~100 mail (ücretsiz)
- **Dakikalık limit**: ~20 mail (ücretsiz)

### **Güvenli Toplu Mail Gönderimi:**
```python
# Rate limiting ile güvenli gönderim
results = mail_sender.send_safe_bulk_mail(
    recipients=recipients,
    subject='Güvenli Toplu Mail',
    body='Bu mail rate limiting ile gönderildi.',
    batch_size=50,  # 50'li gruplar
    delay=60,       # 60 saniye bekleme
    is_html=False
)
```

### **Önerilen Ayarlar:**
- **Grup boyutu**: 25-50 mail
- **Bekleme süresi**: 30-60 saniye
- **Günlük maksimum**: 400 mail (güvenlik payı)

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## İletişim

Sorularınız için GitHub issues kullanın.

---

**Not**: Bu uygulama eğitim amaçlıdır. Ticari kullanım için gerekli izinleri alın ve spam kurallarına uygun hareket edin.
