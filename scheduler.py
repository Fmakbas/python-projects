import schedule
import time
from mail_sender import MailSender
from datetime import datetime
import json

class ScheduledMailSender:
    def __init__(self):
        self.mail_sender = MailSender()
        self.scheduled_jobs = []
    
    def schedule_daily_mail(self, time_str, to_email, subject, body, is_html=False):
        """Günlük mail gönderme zamanlar"""
        job = schedule.every().day.at(time_str).do(
            self.send_scheduled_mail, to_email, subject, body, is_html
        )
        self.scheduled_jobs.append({
            'job': job,
            'type': 'daily',
            'time': time_str,
            'to_email': to_email,
            'subject': subject
        })
        print(f"Günlük mail planlandı: {time_str} - {to_email}")
    
    def schedule_weekly_mail(self, day, time_str, to_email, subject, body, is_html=False):
        """Haftalık mail gönderme zamanlar"""
        job = getattr(schedule.every(), day.lower()).at(time_str).do(
            self.send_scheduled_mail, to_email, subject, body, is_html
        )
        self.scheduled_jobs.append({
            'job': job,
            'type': 'weekly',
            'day': day,
            'time': time_str,
            'to_email': to_email,
            'subject': subject
        })
        print(f"Haftalık mail planlandı: {day} {time_str} - {to_email}")
    
    def send_scheduled_mail(self, to_email, subject, body, is_html=False):
        """Planlanmış mail gönderir"""
        print(f"Planlanmış mail gönderiliyor: {to_email}")
        
        # Tarih değişkenini güncelle
        current_date = datetime.now().strftime("%d.%m.%Y")
        subject = subject.replace("{date}", current_date)
        body = body.replace("{date}", current_date)
        
        success = self.mail_sender.send_mail(to_email, subject, body, is_html=is_html)
        
        if success:
            print(f"✓ Planlanmış mail başarıyla gönderildi: {to_email}")
        else:
            print(f"✗ Planlanmış mail gönderilirken hata: {to_email}")
    
    def start_scheduler(self):
        """Zamanlayıcıyı başlatır"""
        print("Mail zamanlayıcısı başlatılıyor...")
        print("Çıkmak için Ctrl+C tuşlayın")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Her dakika kontrol et
        except KeyboardInterrupt:
            print("\nZamanlayıcı durduruldu.")
    
    def list_scheduled_jobs(self):
        """Planlanmış işleri listeler"""
        if not self.scheduled_jobs:
            print("Planlanmış mail bulunamadı.")
            return
        
        print("\n=== Planlanmış Mailler ===")
        for i, job_info in enumerate(self.scheduled_jobs, 1):
            if job_info['type'] == 'daily':
                print(f"{i}. Günlük - {job_info['time']} - {job_info['to_email']} - {job_info['subject']}")
            elif job_info['type'] == 'weekly':
                print(f"{i}. Haftalık - {job_info['day']} {job_info['time']} - {job_info['to_email']} - {job_info['subject']}")
    
    def remove_scheduled_job(self, index):
        """Planlanmış işi siler"""
        try:
            job_info = self.scheduled_jobs[index]
            schedule.cancel_job(job_info['job'])
            self.scheduled_jobs.pop(index)
            print("Planlanmış mail silindi.")
        except IndexError:
            print("Geçersiz indeks!")

def main():
    """Zamanlayıcı kullanım örneği"""
    scheduler = ScheduledMailSender()
    
    print("=== Otomatik Mail Zamanlayıcı ===")
    print("1. Günlük mail planla")
    print("2. Haftalık mail planla")
    print("3. Planlanmış mailleri listele")
    print("4. Planlanmış mail sil")
    print("5. Zamanlayıcıyı başlat")
    print("6. Çıkış")
    
    while True:
        choice = input("\nSeçiminizi yapın (1-6): ")
        
        if choice == '1':
            time_str = input("Saat (ÖR: 09:00): ")
            to_email = input("Alıcı email: ")
            subject = input("Konu: ")
            body = input("İçerik: ")
            
            scheduler.schedule_daily_mail(time_str, to_email, subject, body)
        
        elif choice == '2':
            day = input("Gün (monday, tuesday, vb.): ")
            time_str = input("Saat (ÖR: 09:00): ")
            to_email = input("Alıcı email: ")
            subject = input("Konu: ")
            body = input("İçerik: ")
            
            scheduler.schedule_weekly_mail(day, time_str, to_email, subject, body)
        
        elif choice == '3':
            scheduler.list_scheduled_jobs()
        
        elif choice == '4':
            scheduler.list_scheduled_jobs()
            if scheduler.scheduled_jobs:
                try:
                    index = int(input("Silinecek mailin numarası: ")) - 1
                    scheduler.remove_scheduled_job(index)
                except ValueError:
                    print("Geçersiz numara!")
        
        elif choice == '5':
            scheduler.start_scheduler()
        
        elif choice == '6':
            print("Çıkış yapılıyor...")
            break
        
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
