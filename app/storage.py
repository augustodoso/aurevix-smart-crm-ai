import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "chat_logs.json"


def save_log(
    user_text: str,
    intent: str,
    reply: str,
    salesforce_created: bool,
    name: str | None = None,
    email: str | None = None,
    company: str | None = None,
    lead_id: str | None = None
) -> None:
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_text": user_text,
        "intent": intent,
        "reply": reply,
        "salesforce_created": salesforce_created,
        "name": name,
        "email": email,
        "company": company,
        "lead_id": lead_id,
    }

    data = []
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []

    data.append(record)

    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )