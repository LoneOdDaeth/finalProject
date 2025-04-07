import smtplib
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()
    server.starttls()
    print("✅ TLS bağlantısı kuruldu.")
