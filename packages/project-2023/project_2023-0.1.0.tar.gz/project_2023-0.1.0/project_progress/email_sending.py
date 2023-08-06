import smtplib
from email.mime.text import MIMEText


def send_email(email_info):
    msg = MIMEText(email_info["text"])

    msg["Subject"] = email_info["Subject"]
    msg["From"] = email_info["From"]
    msg["To"] = email_info["To"]

    smtp_name = email_info.get("smtp_name", "smtp.example.com")
    smtp_port = email_info.get("smtp_port", 587)

    s = smtplib.SMTP(smtp_name, smtp_port)
    s.starttls()
    s.login(email_info["send_email"], email_info["send_pwd"])
    s.send_message(msg)
    s.quit()
