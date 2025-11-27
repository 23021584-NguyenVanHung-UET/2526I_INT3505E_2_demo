# event_queue.py

import threading
import time
from typing import List, Callable, Dict, Any, Optional


class NotificationQueue:
    def __init__(self) -> None:
        self.queue: List[Dict[str, Any]] = []
        self.lock = threading.Lock()

    def push(self, event: Dict[str, Any]) -> None:
        """Push event into queue."""
        with self.lock:
            self.queue.append(event)
            print("📥 Queued event:", event)

    def pop(self) -> Optional[Dict[str, Any]]:
        """Pop event from queue."""
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
        return None


def start_worker(
    queue: NotificationQueue,
    notify_handler: Callable[[Dict[str, Any]], None]
) -> None:
    """Start background worker."""

    def worker() -> None:
        while True:
            event = queue.pop()
            if event is not None:
                print("⚙️ Processing event:", event)
                notify_handler(event)
            time.sleep(1)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
