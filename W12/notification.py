# notification.py

import requests

def send_slack(message: str, webhook_url: str) -> None:
    payload = {"text": message}
    requests.post(webhook_url, json=payload)
    print("📩 Slack sent:", message)


def send_email(to: str, subject: str, body: str) -> None:
    print(f"""
    📧 EMAIL SENT
    To: {to}
    Subject: {subject}
    Body: {body}
    """)


def send_console(message: str) -> None:
    print("🔔 Console Notification:", message)
