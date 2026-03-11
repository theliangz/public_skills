#!/usr/bin/env python3
"""
AI News Daily Email Sender
Sends formatted AI news via email
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from datetime import datetime


def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, html_content):
    """
    Send email using SMTP

    Args:
        smtp_server: SMTP server address (e.g., smtp.gmail.com)
        smtp_port: SMTP port (usually 587 for TLS)
        sender_email: Sender's email address
        sender_password: Sender's email password or app password
        recipient_email: Recipient's email address
        subject: Email subject
        html_content: HTML formatted email body
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Create secure connection
        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print(f"Email sent successfully to {recipient_email}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    # SMTP Configuration - replace with actual values
    # Common SMTP servers:
    # Gmail: smtp.gmail.com:587
    # Outlook: smtp.office365.com:587
    # QQ Mail: smtp.qq.com:587
    # 163 Mail: smtp.163.com:25
    # Aliyun Mail: smtp.aliyun.com:465

    SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
    SMTP_PORT = 587  # Replace with your SMTP port
    SENDER_EMAIL = "your-email@gmail.com"  # Replace with your email
    SENDER_PASSWORD = "your-app-password"  # Replace with your password/app password
    RECIPIENT_EMAIL = "recipient@example.com"  # Replace with recipient email

    # Email content
    date_str = datetime.now().strftime("%Y年%m月%d日")
    subject = f"AI Daily News - {date_str}"

    # Read HTML content from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html_content = f.read()
    else:
        html_content = sys.stdin.read()

    # Send email
    send_email(
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        sender_email=SENDER_EMAIL,
        sender_password=SENDER_PASSWORD,
        recipient_email=RECIPIENT_EMAIL,
        subject=subject,
        html_content=html_content
    )


if __name__ == "__main__":
    main()
