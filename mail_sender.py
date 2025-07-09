import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os
from datetime import datetime
import logging
import time

class MailSender:
    def __init__(self, config_file='config.json'):
        """
        Mail gönderme sınıfı
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        
    def setup_logging(self):
        """Log ayarlarını yapar"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mail_logs.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Yapılandırma dosyasını yükler"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Yapılandırma dosyası yüklenirken hata: {e}")
                return {}
        return {}
    
    def save_config(self, config):
        """Yapılandırma dosyasını kaydeder"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            self.config = config
            self.logger.info("Yapılandırma kaydedildi")
        except Exception as e:
            self.logger.error(f"Yapılandırma kaydedilirken hata: {e}")
    
    def send_mail(self, to_email, subject, body, attachments=None, is_html=False):
        """
        Mail gönderir
        
        Args:
            to_email: Alıcı email adresi (string veya liste)
            subject: Mail başlığı
            body: Mail içeriği
            attachments: Ek dosyalar listesi (opsiyonel)
            is_html: HTML formatında mı (varsayılan: False)
        
        Returns:
            bool: Başarı durumu
        """
        try:
            # SMTP ayarları
            smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.get('smtp_port', 587)
            sender_email = self.config.get('sender_email', '')
            sender_password = self.config.get('sender_password', '')
            
            if not sender_email or not sender_password:
                self.logger.error("Gönderici email ve şifre yapılandırılmamış!")
                return False
            
            # Mail mesajını oluştur
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = subject
            
            # Alıcı adresleri
            if isinstance(to_email, str):
                to_email = [to_email]
            msg['To'] = ', '.join(to_email)
            
            # Mail içeriği
            if is_html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Ek dosyalar
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # SMTP ile gönder
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            
            text = msg.as_string()
            server.sendmail(sender_email, to_email, text)
            server.quit()
            
            self.logger.info(f"Mail başarıyla gönderildi: {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Mail gönderilirken hata: {e}")
            return False
    
    def send_bulk_mail(self, recipients, subject, body, attachments=None, is_html=False):
        """
        Toplu mail gönderir
        
        Args:
            recipients: Alıcı email adresleri listesi
            subject: Mail başlığı
            body: Mail içeriği
            attachments: Ek dosyalar listesi
            is_html: HTML formatında mı
        
        Returns:
            dict: Başarı/hata durumu
        """
        results = {'success': [], 'failed': []}
        
        for email in recipients:
            if self.send_mail(email, subject, body, attachments, is_html):
                results['success'].append(email)
            else:
                results['failed'].append(email)
        
        return results
    
    def send_safe_bulk_mail(self, recipients, subject, body, attachments=None, is_html=False, batch_size=50, delay=60):
        """
        Güvenli toplu mail gönderir (rate limiting ile)
        
        Args:
            recipients: Alıcı email adresleri listesi
            subject: Mail başlığı
            body: Mail içeriği
            attachments: Ek dosyalar listesi
            is_html: HTML formatında mı
            batch_size: Grup başına mail sayısı (varsayılan: 50)
            delay: Gruplar arası bekleme süresi (saniye, varsayılan: 60)
        
        Returns:
            dict: Başarı/hata durumu
        """
        
        results = {'success': [], 'failed': []}
        total_batches = (len(recipients) + batch_size - 1) // batch_size
        
        self.logger.info(f"Güvenli toplu mail başlıyor: {len(recipients)} alıcı, {total_batches} grup")
        
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i+batch_size]
            batch_number = i // batch_size + 1
            
            self.logger.info(f"Grup {batch_number}/{total_batches} gönderiliyor... ({len(batch)} mail)")
            
            batch_results = self.send_bulk_mail(
                recipients=batch,
                subject=subject,
                body=body,
                attachments=attachments,
                is_html=is_html
            )
            
            results['success'].extend(batch_results['success'])
            results['failed'].extend(batch_results['failed'])
            
            # Son grup değilse bekle
            if i + batch_size < len(recipients):
                self.logger.info(f"{delay} saniye bekleniyor...")
                time.sleep(delay)
        
        self.logger.info(f"Güvenli toplu mail tamamlandı: {len(results['success'])} başarılı, {len(results['failed'])} başarısız")
        return results
    
    def get_mail_templates(self):
        """Hazır mail şablonlarını döndürür"""
        return {
            'welcome': {
                'subject': 'Hoş Geldiniz!',
                'body': '''
Merhaba {name},

Sisteme hoş geldiniz! Hesabınız başarıyla oluşturuldu.

İyi günler,
{company}
                '''.strip()
            },
            'reminder': {
                'subject': 'Hatırlatma',
                'body': '''
Merhaba,

Bu bir hatırlatma mailidir. Lütfen unutmayın:
{reminder_text}

Teşekkürler,
{company}
                '''.strip()
            },
            'newsletter': {
                'subject': 'Haber Bülteni - {date}',
                'body': '''
<h2>Haber Bülteni</h2>
<p>Merhaba,</p>
<p>Bu ayın haberlerini sizlerle paylaşmak istiyoruz:</p>
<ul>
    <li>{news_item_1}</li>
    <li>{news_item_2}</li>
    <li>{news_item_3}</li>
</ul>
<p>Saygılarımızla,<br>{company}</p>
                '''.strip()
            }
        }
