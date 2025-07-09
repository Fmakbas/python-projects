import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from mail_sender import MailSender
import threading
import json
import os

class MailSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Otomatik Mail Gönderme Uygulaması")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Mail sender sınıfı
        self.mail_sender = MailSender()
        
        # Değişkenler
        self.attachments = []
        self.bulk_attachments = []  # Toplu mail için ek dosyalar
        
        # GUI'yi oluştur
        self.create_widgets()
        
        # Kayıtlı yapılandırmayı yükle
        self.load_saved_config()
    
    def create_widgets(self):
        """GUI bileşenlerini oluşturur"""
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab widget
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Yapılandırma sekmesi
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Yapılandırma")
        self.create_config_tab(config_frame)
        
        # Mail gönderme sekmesi
        send_frame = ttk.Frame(notebook)
        notebook.add(send_frame, text="Mail Gönder")
        self.create_send_tab(send_frame)
        
        # Toplu mail sekmesi
        bulk_frame = ttk.Frame(notebook)
        notebook.add(bulk_frame, text="Toplu Mail")
        self.create_bulk_tab(bulk_frame)
        
        # Şablonlar sekmesi
        template_frame = ttk.Frame(notebook)
        notebook.add(template_frame, text="Şablonlar")
        self.create_template_tab(template_frame)
        
        # Grid yapılandırması
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def create_config_tab(self, parent):
        """Yapılandırma sekmesini oluşturur"""
        # Başlık
        title_label = ttk.Label(parent, text="SMTP Yapılandırması", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # SMTP Server
        ttk.Label(parent, text="SMTP Server:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.smtp_server_var = tk.StringVar(value="smtp.gmail.com")
        ttk.Entry(parent, textvariable=self.smtp_server_var, width=30).grid(row=1, column=1, pady=5)
        
        # SMTP Port
        ttk.Label(parent, text="SMTP Port:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.smtp_port_var = tk.StringVar(value="587")
        ttk.Entry(parent, textvariable=self.smtp_port_var, width=30).grid(row=2, column=1, pady=5)
        
        # Sender Email
        ttk.Label(parent, text="Gönderici Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.sender_email_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.sender_email_var, width=30).grid(row=3, column=1, pady=5)
        
        # Sender Password
        ttk.Label(parent, text="Gönderici Şifre:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sender_password_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.sender_password_var, width=30, show="*").grid(row=4, column=1, pady=5)
        
        # Kaydet butonu
        ttk.Button(parent, text="Yapılandırmayı Kaydet", command=self.save_config).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Bilgi metni
        info_text = """
Gmail için yapılandırma:
- SMTP Server: smtp.gmail.com
- SMTP Port: 587
- 2FA aktifse uygulama şifresi kullanın
- Güvenlik ayarlarında "Az güvenli uygulamalara izin ver" seçeneğini açın

Outlook için yapılandırma:
- SMTP Server: smtp-mail.outlook.com
- SMTP Port: 587
        """
        info_label = ttk.Label(parent, text=info_text, font=('Arial', 9), foreground='gray')
        info_label.grid(row=6, column=0, columnspan=2, pady=10)
    
    def create_send_tab(self, parent):
        """Mail gönderme sekmesini oluşturur"""
        # Alıcı
        ttk.Label(parent, text="Alıcı Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.to_email_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.to_email_var, width=50).grid(row=0, column=1, pady=5)
        
        # Konu
        ttk.Label(parent, text="Konu:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.subject_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.subject_var, width=50).grid(row=1, column=1, pady=5)
        
        # İçerik
        ttk.Label(parent, text="İçerik:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.body_text = ScrolledText(parent, height=10, width=60)
        self.body_text.grid(row=2, column=1, pady=5)
        
        # HTML checkbox
        self.is_html_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="HTML formatında", variable=self.is_html_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Ek dosyalar
        ttk.Label(parent, text="Ek Dosyalar:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.attachments_listbox = tk.Listbox(parent, height=3, width=40)
        self.attachments_listbox.grid(row=4, column=1, pady=5)
        
        # Ek dosya butonları
        attachment_frame = ttk.Frame(parent)
        attachment_frame.grid(row=5, column=1, pady=5)
        ttk.Button(attachment_frame, text="Dosya Ekle", command=self.add_attachment).pack(side=tk.LEFT, padx=5)
        ttk.Button(attachment_frame, text="Dosya Sil", command=self.remove_attachment).pack(side=tk.LEFT, padx=5)
        
        # Gönder butonu
        ttk.Button(parent, text="Mail Gönder", command=self.send_single_mail).grid(row=6, column=0, columnspan=2, pady=20)
    
    def create_bulk_tab(self, parent):
        """Toplu mail sekmesini oluşturur"""
        # Alıcı listesi
        ttk.Label(parent, text="Alıcı Email Listesi (her satırda bir email):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.recipients_text = ScrolledText(parent, height=6, width=60)
        self.recipients_text.grid(row=0, column=1, pady=5)
        
        # Konu
        ttk.Label(parent, text="Konu:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bulk_subject_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.bulk_subject_var, width=50).grid(row=1, column=1, pady=5)
        
        # İçerik
        ttk.Label(parent, text="İçerik:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.bulk_body_text = ScrolledText(parent, height=8, width=60)
        self.bulk_body_text.grid(row=2, column=1, pady=5)
        
        # HTML checkbox
        self.bulk_is_html_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="HTML formatında", variable=self.bulk_is_html_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Ek dosyalar (toplu mail için)
        ttk.Label(parent, text="Ek Dosyalar:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.bulk_attachments_listbox = tk.Listbox(parent, height=3, width=40)
        self.bulk_attachments_listbox.grid(row=4, column=1, pady=5)
        
        # Ek dosya butonları (toplu mail için)
        bulk_attachment_frame = ttk.Frame(parent)
        bulk_attachment_frame.grid(row=5, column=1, pady=5)
        ttk.Button(bulk_attachment_frame, text="Dosya Ekle", command=self.add_bulk_attachment).pack(side=tk.LEFT, padx=5)
        ttk.Button(bulk_attachment_frame, text="Dosya Sil", command=self.remove_bulk_attachment).pack(side=tk.LEFT, padx=5)
        
        # Güvenli gönderim seçenekleri
        options_frame = ttk.LabelFrame(parent, text="Güvenli Gönderim Seçenekleri", padding="5")
        options_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Güvenli gönderim checkbox
        self.safe_sending_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Güvenli gönderim (rate limiting)", variable=self.safe_sending_var).grid(row=0, column=0, sticky=tk.W)
        
        # Grup boyutu
        ttk.Label(options_frame, text="Grup boyutu:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.batch_size_var = tk.StringVar(value="50")
        ttk.Entry(options_frame, textvariable=self.batch_size_var, width=10).grid(row=1, column=1, pady=5)
        
        # Bekleme süresi
        ttk.Label(options_frame, text="Bekleme süresi (saniye):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.delay_var = tk.StringVar(value="60")
        ttk.Entry(options_frame, textvariable=self.delay_var, width=10).grid(row=2, column=1, pady=5)
        
        # Gönder butonu
        ttk.Button(parent, text="Toplu Mail Gönder", command=self.send_bulk_mail).grid(row=7, column=0, columnspan=2, pady=20)
        
        # Sonuç alanı
        ttk.Label(parent, text="Sonuçlar:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.results_text = ScrolledText(parent, height=6, width=60)
        self.results_text.grid(row=8, column=1, pady=5)
    
    def create_template_tab(self, parent):
        """Şablonlar sekmesini oluşturur"""
        # Şablon seçimi
        ttk.Label(parent, text="Şablon Seç:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar()
        template_combo = ttk.Combobox(parent, textvariable=self.template_var, width=30)
        template_combo['values'] = list(self.mail_sender.get_mail_templates().keys())
        template_combo.grid(row=0, column=1, pady=5)
        
        # Şablonu yükle butonu
        ttk.Button(parent, text="Şablonu Yükle", command=self.load_template).grid(row=0, column=2, pady=5)
        
        # Şablon içeriği
        ttk.Label(parent, text="Şablon İçeriği:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.template_text = ScrolledText(parent, height=15, width=70)
        self.template_text.grid(row=1, column=1, columnspan=2, pady=5)
        
        # Değişken bilgisi
        info_text = """
Şablonlarda kullanılabilecek değişkenler:
{name} - İsim
{company} - Şirket adı
{date} - Tarih
{reminder_text} - Hatırlatma metni
{news_item_1}, {news_item_2}, {news_item_3} - Haber maddeleri
        """
        info_label = ttk.Label(parent, text=info_text, font=('Arial', 9), foreground='gray')
        info_label.grid(row=2, column=1, columnspan=2, pady=10)
    
    def save_config(self):
        """Yapılandırmayı kaydeder"""
        config = {
            'smtp_server': self.smtp_server_var.get(),
            'smtp_port': int(self.smtp_port_var.get()),
            'sender_email': self.sender_email_var.get(),
            'sender_password': self.sender_password_var.get()
        }
        
        self.mail_sender.save_config(config)
        messagebox.showinfo("Başarılı", "Yapılandırma kaydedildi!")
    
    def load_saved_config(self):
        """Kayıtlı yapılandırmayı yükler"""
        config = self.mail_sender.config
        if config:
            self.smtp_server_var.set(config.get('smtp_server', 'smtp.gmail.com'))
            self.smtp_port_var.set(str(config.get('smtp_port', 587)))
            self.sender_email_var.set(config.get('sender_email', ''))
            self.sender_password_var.set(config.get('sender_password', ''))
    
    def add_attachment(self):
        """Ek dosya ekler"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attachments.append(file_path)
            self.attachments_listbox.insert(tk.END, os.path.basename(file_path))
    
    def remove_attachment(self):
        """Ek dosya siler"""
        selection = self.attachments_listbox.curselection()
        if selection:
            index = selection[0]
            self.attachments_listbox.delete(index)
            self.attachments.pop(index)
    
    def add_bulk_attachment(self):
        """Toplu mail için ek dosya ekler"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.bulk_attachments.append(file_path)
            self.bulk_attachments_listbox.insert(tk.END, os.path.basename(file_path))
    
    def remove_bulk_attachment(self):
        """Toplu mail için ek dosya siler"""
        selection = self.bulk_attachments_listbox.curselection()
        if selection:
            index = selection[0]
            self.bulk_attachments_listbox.delete(index)
            self.bulk_attachments.pop(index)
    
    def send_single_mail(self):
        """Tek mail gönderir"""
        if not self.to_email_var.get() or not self.subject_var.get():
            messagebox.showerror("Hata", "Alıcı email ve konu alanları zorunludur!")
            return
        
        def send_mail_thread():
            success = self.mail_sender.send_mail(
                to_email=self.to_email_var.get(),
                subject=self.subject_var.get(),
                body=self.body_text.get('1.0', tk.END),
                attachments=self.attachments if self.attachments else None,
                is_html=self.is_html_var.get()
            )
            
            if success:
                messagebox.showinfo("Başarılı", "Mail başarıyla gönderildi!")
            else:
                messagebox.showerror("Hata", "Mail gönderilirken hata oluştu!")
        
        threading.Thread(target=send_mail_thread).start()
    
    def send_bulk_mail(self):
        """Toplu mail gönderir"""
        recipients_text = self.recipients_text.get('1.0', tk.END).strip()
        if not recipients_text or not self.bulk_subject_var.get():
            messagebox.showerror("Hata", "Alıcı listesi ve konu alanları zorunludur!")
            return
        
        recipients = [email.strip() for email in recipients_text.split('\n') if email.strip()]
        
        def send_bulk_mail_thread():
            # Güvenli gönderim ayarları
            safe_sending = self.safe_sending_var.get()
            batch_size = int(self.batch_size_var.get()) if self.batch_size_var.get().isdigit() else 50
            delay = int(self.delay_var.get()) if self.delay_var.get().isdigit() else 60
            
            if safe_sending:
                results = self.mail_sender.send_safe_bulk_mail(
                    recipients=recipients,
                    subject=self.bulk_subject_var.get(),
                    body=self.bulk_body_text.get('1.0', tk.END),
                    attachments=self.bulk_attachments if self.bulk_attachments else None,
                    is_html=self.bulk_is_html_var.get(),
                    batch_size=batch_size,
                    delay=delay
                )
            else:
                results = self.mail_sender.send_bulk_mail(
                    recipients=recipients,
                    subject=self.bulk_subject_var.get(),
                    body=self.bulk_body_text.get('1.0', tk.END),
                    attachments=self.bulk_attachments if self.bulk_attachments else None,
                    is_html=self.bulk_is_html_var.get()
                )
            
            # Sonuçları göster
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, f"Başarılı: {len(results['success'])} mail\n")
            self.results_text.insert(tk.END, f"Başarısız: {len(results['failed'])} mail\n\n")
            
            if results['success']:
                self.results_text.insert(tk.END, "Başarılı gönderimler:\n")
                for email in results['success']:
                    self.results_text.insert(tk.END, f"✓ {email}\n")
            
            if results['failed']:
                self.results_text.insert(tk.END, "\nBaşarısız gönderimler:\n")
                for email in results['failed']:
                    self.results_text.insert(tk.END, f"✗ {email}\n")
            
            messagebox.showinfo("Tamamlandı", f"Toplu mail gönderimi tamamlandı!\nBaşarılı: {len(results['success'])}, Başarısız: {len(results['failed'])}")
        
        threading.Thread(target=send_bulk_mail_thread).start()
    
    def load_template(self):
        """Seçili şablonu yükler"""
        template_name = self.template_var.get()
        if not template_name:
            messagebox.showerror("Hata", "Lütfen bir şablon seçin!")
            return
        
        templates = self.mail_sender.get_mail_templates()
        template = templates.get(template_name)
        
        if template:
            self.template_text.delete('1.0', tk.END)
            self.template_text.insert(tk.END, f"Konu: {template['subject']}\n\n")
            self.template_text.insert(tk.END, f"İçerik:\n{template['body']}")

def main():
    root = tk.Tk()
    app = MailSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
