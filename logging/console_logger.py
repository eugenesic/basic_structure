from datetime import datetime


def log_event(event_type: str, payload):
    ts = datetime.utcnow().isoformat()
    print(f"[{ts}] {event_type}: {payload}")

