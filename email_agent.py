import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "put_your_email@gmail.com"      # <-- PUT YOUR GMAIL
APP_PASSWORD = "put_your_app_password"      # <-- PUT 16 CHAR APP PASSWORD


def send_email(recipient_email, title, decision, risk_score):

    subject = f"AutoGov-X Decision: {decision}"

    body = f"""
Dear Researcher,

Your submission titled "{title}" has been reviewed.

Final Decision: {decision}
Risk Score: {risk_score}

Thank you for using AutoGov-X Autonomous Governance Engine.

Regards,
AutoGov-X Committee
"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False