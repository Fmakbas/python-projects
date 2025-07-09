from mail_sender import MailSender
from datetime import datetime, timedelta
import json

# Örnek kullanım scriptleri

def example_single_mail():
    """Tek mail gönderme örneği"""
    print("=== Tek Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    # Yapılandırma (gerçek değerlerinizle değiştirin)
    config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'your_email@gmail.com',
        'sender_password': 'your_app_password'
    }
    mail_sender.save_config(config)
    
    # Mail gönder
    success = mail_sender.send_mail(
        to_email='recipient@example.com',
        subject='Test Mail',
        body='Bu bir test mailidir.',
        is_html=False
    )
    
    if success:
        print("✓ Mail başarıyla gönderildi!")
    else:
        print("✗ Mail gönderilirken hata oluştu!")

def example_html_mail():
    """HTML mail gönderme örneği"""
    print("=== HTML Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    html_body = """
    <html>
    <body>
        <h2>Merhaba!</h2>
        <p>Bu bir <b>HTML</b> mail örneğidir.</p>
        <ul>
            <li>Madde 1</li>
            <li>Madde 2</li>
            <li>Madde 3</li>
        </ul>
        <p>Saygılarımızla,<br>
        <a href="https://example.com">Şirketimiz</a></p>
    </body>
    </html>
    """
    
    success = mail_sender.send_mail(
        to_email='recipient@example.com',
        subject='HTML Test Mail',
        body=html_body,
        is_html=True
    )
    
    print("HTML mail gönderildi!" if success else "HTML mail gönderilirken hata!")

def example_bulk_mail():
    """Toplu mail gönderme örneği"""
    print("=== Toplu Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    recipients = [
        'user1@example.com',
        'user2@example.com',
        'user3@example.com'
    ]
    
    results = mail_sender.send_bulk_mail(
        recipients=recipients,
        subject='Toplu Mail Test',
        body='Bu toplu mail gönderim testidir.',
        is_html=False
    )
    
    print(f"Başarılı: {len(results['success'])} mail")
    print(f"Başarısız: {len(results['failed'])} mail")
    
    if results['failed']:
        print("Başarısız gönderimler:")
        for email in results['failed']:
            print(f"  - {email}")

def example_bulk_mail_with_attachments():
    """Ek dosyalı toplu mail gönderme örneği"""
    print("=== Ek Dosyalı Toplu Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    recipients = [
        'user1@example.com',
        'user2@example.com',
        'user3@example.com'
    ]
    
    # Örnek ek dosya oluştur
    attachment_file = 'toplu_mail_ek.txt'
    with open(attachment_file, 'w', encoding='utf-8') as f:
        f.write('Bu toplu mail için ek dosyadır.\n')
        f.write('Tüm alıcılar bu dosyayı alacak.\n')
        f.write('Tarih: 2025-07-08')
    
    results = mail_sender.send_bulk_mail(
        recipients=recipients,
        subject='Ek Dosyalı Toplu Mail',
        body='Bu toplu mail ek dosya içermektedir. Lütfen ek dosyayı kontrol edin.',
        attachments=[attachment_file],
        is_html=False
    )
    
    print(f"Ek dosyalı toplu mail gönderildi!")
    print(f"Başarılı: {len(results['success'])} mail")
    print(f"Başarısız: {len(results['failed'])} mail")
    
    if results['failed']:
        print("Başarısız gönderimler:")
        for email in results['failed']:
            print(f"  - {email}")

def example_template_mail():
    """Şablon mail gönderme örneği"""
    print("=== Şablon Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    # Hoş geldin maili
    templates = mail_sender.get_mail_templates()
    welcome_template = templates['welcome']
    
    # Şablon değişkenlerini doldur
    subject = welcome_template['subject']
    body = welcome_template['body'].format(
        name='Ahmet Yılmaz',
        company='ABC Şirketi'
    )
    
    success = mail_sender.send_mail(
        to_email='ahmet@example.com',
        subject=subject,
        body=body,
        is_html=False
    )
    
    print("Şablon mail gönderildi!" if success else "Şablon mail gönderilirken hata!")

def example_newsletter():
    """Newsletter gönderme örneği"""
    print("=== Newsletter Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    templates = mail_sender.get_mail_templates()
    newsletter_template = templates['newsletter']
    
    # Newsletter içeriğini doldur
    today = datetime.now().strftime("%d.%m.%Y")
    
    subject = newsletter_template['subject'].format(date=today)
    body = newsletter_template['body'].format(
        news_item_1='Yeni ürün lansmanı gerçekleştirildi',
        news_item_2='Şirket büyüme hedeflerine ulaştı',
        news_item_3='Müşteri memnuniyeti %95 seviyesinde',
        company='ABC Şirketi',
        date=today
    )
    
    # Newsletter abonelerine gönder
    newsletter_subscribers = [
        'subscriber1@example.com',
        'subscriber2@example.com',
        'subscriber3@example.com'
    ]
    
    results = mail_sender.send_bulk_mail(
        recipients=newsletter_subscribers,
        subject=subject,
        body=body,
        is_html=True
    )
    
    print(f"Newsletter gönderildi! Başarılı: {len(results['success'])}, Başarısız: {len(results['failed'])}")

def example_attachment_mail():
    """Ek dosyalı mail gönderme örneği"""
    print("=== Ek Dosyalı Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    # Örnek dosya oluştur (test için)
    test_file = 'test_attachment.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('Bu bir test ek dosyasıdır.')
    
    success = mail_sender.send_mail(
        to_email='recipient@example.com',
        subject='Ek Dosyalı Mail',
        body='Bu mail ek dosya içermektedir.',
        attachments=[test_file],
        is_html=False
    )
    
    print("Ek dosyalı mail gönderildi!" if success else "Ek dosyalı mail gönderilirken hata!")

def example_reminder_system():
    """Hatırlatma sistemi örneği"""
    print("=== Hatırlatma Sistemi Örneği ===")
    
    mail_sender = MailSender()
    
    # Farklı hatırlatma türleri
    reminders = [
        {
            'to_email': 'manager@example.com',
            'reminder_text': 'Yarın toplantı var (14:00)',
            'company': 'ABC Şirketi'
        },
        {
            'to_email': 'employee@example.com',
            'reminder_text': 'Rapor teslim tarihi bugün',
            'company': 'ABC Şirketi'
        }
    ]
    
    templates = mail_sender.get_mail_templates()
    reminder_template = templates['reminder']
    
    for reminder in reminders:
        subject = reminder_template['subject']
        body = reminder_template['body'].format(**reminder)
        
        success = mail_sender.send_mail(
            to_email=reminder['to_email'],
            subject=subject,
            body=body,
            is_html=False
        )
        
        print(f"Hatırlatma gönderildi: {reminder['to_email']} - {'✓' if success else '✗'}")

def example_personalized_bulk_mail():
    """Kişiselleştirilmiş toplu mail örneği"""
    print("=== Kişiselleştirilmiş Toplu Mail Örneği ===")
    
    mail_sender = MailSender()
    
    # Kişisel bilgiler
    customers = [
        {'email': 'ali@example.com', 'name': 'Ali Yılmaz', 'product': 'Telefon'},
        {'email': 'ayse@example.com', 'name': 'Ayşe Kaya', 'product': 'Laptop'},
        {'email': 'mehmet@example.com', 'name': 'Mehmet Demir', 'product': 'Tablet'}
    ]
    
    # Her müşteri için kişisel mail
    for customer in customers:
        subject = f"Merhaba {customer['name']}, {customer['product']} siparişiniz hazır!"
        body = f"""
Sayın {customer['name']},

{customer['product']} siparişiniz hazırlandı ve kargoya verildi.
Takip numaranız: TK{hash(customer['email']) % 100000}

Teşekkürler,
E-Ticaret Ekibi
        """.strip()
        
        success = mail_sender.send_mail(
            to_email=customer['email'],
            subject=subject,
            body=body,
            is_html=False
        )
        
        print(f"Kişisel mail gönderildi: {customer['name']} - {'✓' if success else '✗'}")

def example_safe_bulk_mail():
    """Güvenli toplu mail gönderme örneği"""
    print("=== Güvenli Toplu Mail Gönderme Örneği ===")
    
    mail_sender = MailSender()
    
    # Büyük bir alıcı listesi simülasyonu
    recipients = [
        f'user{i}@example.com' for i in range(1, 151)  # 150 kişi
    ]
    
    print(f"Büyük alıcı listesi: {len(recipients)} kişi")
    
    # Güvenli gönderim
    results = mail_sender.send_safe_bulk_mail(
        recipients=recipients,
        subject='Güvenli Toplu Mail Test',
        body='Bu mail rate limiting ile gönderildi.',
        batch_size=25,  # 25'li gruplar
        delay=30,       # 30 saniye bekleme
        is_html=False
    )
    
    print(f"Güvenli toplu mail tamamlandı!")
    print(f"Başarılı: {len(results['success'])} mail")
    print(f"Başarısız: {len(results['failed'])} mail")
    print(f"Toplam süre: ~{(len(recipients) // 25) * 30} saniye")

def main():
    """Ana örnek menüsü"""
    print("=== Mail Gönderme Örnekleri ===")
    print("1. Tek mail gönder")
    print("2. HTML mail gönder")
    print("3. Toplu mail gönder")
    print("4. Ek dosyalı toplu mail gönder")
    print("5. Şablon mail gönder")
    print("6. Newsletter gönder")
    print("7. Ek dosyalı mail gönder")
    print("8. Hatırlatma sistemi")
    print("9. Kişiselleştirilmiş toplu mail")
    print("10. Güvenli toplu mail gönder")
    print("11. Çıkış")
    
    while True:
        choice = input("\nHangi örneği çalıştırmak istiyorsunuz? (1-11): ")
        
        if choice == '1':
            example_single_mail()
        elif choice == '2':
            example_html_mail()
        elif choice == '3':
            example_bulk_mail()
        elif choice == '4':
            example_bulk_mail_with_attachments()
        elif choice == '5':
            example_template_mail()
        elif choice == '6':
            example_newsletter()
        elif choice == '7':
            example_attachment_mail()
        elif choice == '8':
            example_reminder_system()
        elif choice == '9':
            example_personalized_bulk_mail()
        elif choice == '10':
            example_safe_bulk_mail()
        elif choice == '11':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
