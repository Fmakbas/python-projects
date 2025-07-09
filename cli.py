from mail_sender import MailSender
from datetime import datetime
import time

def main():
    """
    Komut satırı kullanım örneği
    """
    # Mail sender'ı başlat
    mail_sender = MailSender()
    
    # Yapılandırma örneği (ilk kullanımda)
    config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'your_email@gmail.com',  # Buraya kendi email adresinizi yazın
        'sender_password': 'your_app_password'   # Buraya app password'unuzu yazın
    }
    
    # Yapılandırmayı kaydet (isteğe bağlı)
    # mail_sender.save_config(config)
    
    print("=== Otomatik Mail Gönderme Uygulaması ===")
    print("1. Tek mail gönder")
    print("2. Toplu mail gönder")
    print("3. Güvenli toplu mail gönder")
    print("4. Şablon kullanarak mail gönder")
    print("5. Çıkış")
    
    while True:
        choice = input("\nSeçiminizi yapın (1-5): ")
        
        if choice == '1':
            send_single_mail(mail_sender)
        elif choice == '2':
            send_bulk_mail(mail_sender)
        elif choice == '3':
            send_safe_bulk_mail(mail_sender)
        elif choice == '4':
            send_template_mail(mail_sender)
        elif choice == '5':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")

def send_single_mail(mail_sender):
    """Tek mail gönderir"""
    print("\n--- Tek Mail Gönderme ---")
    
    to_email = input("Alıcı email adresi: ")
    subject = input("Konu: ")
    body = input("İçerik: ")
    
    html_choice = input("HTML formatında mı? (e/h): ").lower()
    is_html = html_choice == 'e'
    
    # Ek dosya
    attachment_choice = input("Ek dosya eklemek ister misiniz? (e/h): ").lower()
    attachments = None
    if attachment_choice == 'e':
        attachment_path = input("Dosya yolu: ")
        attachments = [attachment_path]
    
    print("Mail gönderiliyor...")
    success = mail_sender.send_mail(to_email, subject, body, attachments, is_html)
    
    if success:
        print("✓ Mail başarıyla gönderildi!")
    else:
        print("✗ Mail gönderilirken hata oluştu!")

def send_bulk_mail(mail_sender):
    """Toplu mail gönderir"""
    print("\n--- Toplu Mail Gönderme ---")
    
    recipients = []
    print("Alıcı email adreslerini girin (bitirmek için 'tamam' yazın):")
    while True:
        email = input("Email: ")
        if email.lower() == 'tamam':
            break
        recipients.append(email)
    
    subject = input("Konu: ")
    body = input("İçerik: ")
    
    html_choice = input("HTML formatında mı? (e/h): ").lower()
    is_html = html_choice == 'e'
    
    # Ek dosyalar (toplu mail için)
    bulk_attachments = []
    attachment_choice = input("Toplu mail için ek dosya eklemek ister misiniz? (e/h): ").lower()
    if attachment_choice == 'e':
        print("Ek dosya yollarını girin (bitirmek için 'tamam' yazın):")
        while True:
            attachment_path = input("Dosya yolu: ")
            if attachment_path.lower() == 'tamam':
                break
            bulk_attachments.append(attachment_path)
    
    print("Toplu mail gönderiliyor...")
    results = mail_sender.send_bulk_mail(
        recipients, 
        subject, 
        body, 
        attachments=bulk_attachments if bulk_attachments else None,
        is_html=is_html
    )
    
    print(f"\n✓ Başarılı: {len(results['success'])} mail")
    print(f"✗ Başarısız: {len(results['failed'])} mail")
    
    if results['failed']:
        print("\nBaşarısız gönderimler:")
        for email in results['failed']:
            print(f"  - {email}")

def send_safe_bulk_mail(mail_sender):
    """Güvenli toplu mail gönderir"""
    print("\n--- Güvenli Toplu Mail Gönderme ---")
    print("Bu özellik rate limiting kullanarak Gmail limitlerini aşmadan mail gönderir.")
    
    recipients = []
    print("Alıcı email adreslerini girin (bitirmek için 'tamam' yazın):")
    while True:
        email = input("Email: ")
        if email.lower() == 'tamam':
            break
        recipients.append(email)
    
    if not recipients:
        print("Alıcı listesi boş!")
        return
    
    print(f"Toplam alıcı: {len(recipients)}")
    
    subject = input("Konu: ")
    body = input("İçerik: ")
    
    html_choice = input("HTML formatında mı? (e/h): ").lower()
    is_html = html_choice == 'e'
    
    # Güvenli gönderim ayarları
    batch_size = input("Grup boyutu (varsayılan: 50): ")
    batch_size = int(batch_size) if batch_size.isdigit() else 50
    
    delay = input("Gruplar arası bekleme süresi (saniye, varsayılan: 60): ")
    delay = int(delay) if delay.isdigit() else 60
    
    # Ek dosyalar (toplu mail için)
    bulk_attachments = []
    attachment_choice = input("Ek dosya eklemek ister misiniz? (e/h): ").lower()
    if attachment_choice == 'e':
        print("Ek dosya yollarını girin (bitirmek için 'tamam' yazın):")
        while True:
            attachment_path = input("Dosya yolu: ")
            if attachment_path.lower() == 'tamam':
                break
            bulk_attachments.append(attachment_path)
    
    print(f"\nGüvenli toplu mail gönderiliyor...")
    print(f"Grup boyutu: {batch_size}")
    print(f"Bekleme süresi: {delay} saniye")
    print(f"Tahmini süre: {(len(recipients) // batch_size) * delay} saniye")
    
    results = mail_sender.send_safe_bulk_mail(
        recipients=recipients,
        subject=subject,
        body=body,
        attachments=bulk_attachments if bulk_attachments else None,
        is_html=is_html,
        batch_size=batch_size,
        delay=delay
    )
    
    print(f"\n✓ Başarılı: {len(results['success'])} mail")
    print(f"✗ Başarısız: {len(results['failed'])} mail")
    
    if results['failed']:
        print("\nBaşarısız gönderimler:")
        for email in results['failed']:
            print(f"  - {email}")

def send_template_mail(mail_sender):
    """Şablon kullanarak mail gönderir"""
    print("\n--- Şablon Mail Gönderme ---")
    
    templates = mail_sender.get_mail_templates()
    print("Mevcut şablonlar:")
    for i, template_name in enumerate(templates.keys(), 1):
        print(f"{i}. {template_name}")
    
    choice = input("Şablon seçin (1-{}): ".format(len(templates)))
    template_names = list(templates.keys())
    
    try:
        template_index = int(choice) - 1
        template_name = template_names[template_index]
        template = templates[template_name]
    except (ValueError, IndexError):
        print("Geçersiz seçim!")
        return
    
    print(f"\nSeçilen şablon: {template_name}")
    print(f"Konu: {template['subject']}")
    print(f"İçerik: {template['body']}")
    
    # Değişkenleri doldur
    variables = {}
    if '{name}' in template['body'] or '{name}' in template['subject']:
        variables['name'] = input("İsim: ")
    if '{company}' in template['body'] or '{company}' in template['subject']:
        variables['company'] = input("Şirket adı: ")
    if '{date}' in template['body'] or '{date}' in template['subject']:
        variables['date'] = datetime.now().strftime("%d.%m.%Y")
    if '{reminder_text}' in template['body']:
        variables['reminder_text'] = input("Hatırlatma metni: ")
    
    # Newsletter için özel değişkenler
    if template_name == 'newsletter':
        variables['news_item_1'] = input("Haber 1: ")
        variables['news_item_2'] = input("Haber 2: ")
        variables['news_item_3'] = input("Haber 3: ")
    
    # Değişkenleri uygula
    subject = template['subject'].format(**variables)
    body = template['body'].format(**variables)
    
    to_email = input("Alıcı email adresi: ")
    
    print("Mail gönderiliyor...")
    success = mail_sender.send_mail(to_email, subject, body, is_html=template_name == 'newsletter')
    
    if success:
        print("✓ Mail başarıyla gönderildi!")
    else:
        print("✗ Mail gönderilirken hata oluştu!")

if __name__ == "__main__":
    main()
