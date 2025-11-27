# main.py

from fastapi import FastAPI, Request
from typing import Dict, Any

from event_queue import NotificationQueue, start_worker
from notification import send_slack, send_email, send_console
import os

SLACK_WEBHOOK_URL: str | None = os.getenv("SLACK_WEBHOOK_URL")

app = FastAPI(title="Webhook Notification Demo")

queue = NotificationQueue()


def notify_handler(event: Dict[str, Any]) -> None:
    event_type: str = event.get("type", "unknown")
    data: Dict[str, Any] = event.get("data", {})

    msg: str = f"Event: {event_type}\nData: {data}"

    send_console(msg)

    if SLACK_WEBHOOK_URL:
        send_slack(msg, SLACK_WEBHOOK_URL)

    send_email("admin@example.com", f"Event {event_type}", msg)


# Start background worker
start_worker(queue, notify_handler)


@app.post("/webhook")
async def receive_webhook(request: Request) -> Dict[str, Any]:
    payload: Dict[str, Any] = await request.json()
    print("📨 Webhook received:", payload)

    queue.push(payload)
    return {"status": "ok", "received": True}
