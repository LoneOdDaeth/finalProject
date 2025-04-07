import smtplib
import ssl
from email.message import EmailMessage
from typing import List, Optional, Tuple
from database.mongo_operations import get_smtp_settings

def send_mail(
    sender_email: str,
    to_email: str,
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None
) -> Tuple[bool, str]:
    smtp_settings = get_smtp_settings(sender_email)
    if not smtp_settings:
        return False, "❌ SMTP ayarları bulunamadı. Lütfen sistem ayarlarından tanımlayın."

    host = smtp_settings["host"]
    port = smtp_settings["port"]
    tls = smtp_settings["tls"]
    username = smtp_settings["username"]
    password = smtp_settings["password"]

    # Güvenlik: TLS değeri normalize edilsin
    tls = str(tls).lower() == "true"

    # Uyum kontrolü
    if port == 587 and not tls:
        return False, "❌ Port 587 kullanıyorsanız TLS aktif olmalıdır."
    if port == 465 and tls:
        return False, "❌ Port 465 SSL içindir. TLS kullanıyorsanız port 587 kullanmalısınız."

    try:
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        if attachments:
            for file_path in attachments:
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_name = file_path.split("/")[-1]
                        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
                except Exception as e:
                    return False, f"❌ Ek dosya okunamadı: {file_path}\nHata: {str(e)}"

        if tls:
            context = ssl.create_default_context()
            with smtplib.SMTP(host, port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.login(username, password)
                server.send_message(msg)
        else:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)

        return True, "✅ Mail başarıyla gönderildi."

    except smtplib.SMTPAuthenticationError:
        return False, "❌ Kimlik doğrulama hatası: Kullanıcı adı veya şifre hatalı olabilir."
    except smtplib.SMTPConnectError:
        return False, "❌ SMTP sunucusuna bağlanılamadı. Port ve host bilgilerini kontrol edin."
    except Exception as e:
        return False, f"❌ Mail gönderim hatası: {str(e)}"
