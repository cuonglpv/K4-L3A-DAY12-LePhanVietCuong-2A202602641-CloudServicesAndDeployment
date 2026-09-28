"""Small, cloud-friendly JSON logger."""

import json
from datetime import datetime, timezone
from typing import Any


def log_event(event: str, level: str = "info", **fields: Any) -> str:
    """Write exactly one JSON object to stdout for a structured log event."""
    payload = {
        "event": event,
        "level": level.lower(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **fields,
    }
    # stdout is what Docker and most cloud platforms collect.  ``print`` is
    # used intentionally: each invocation must produce one physical line even
    # before the host logging framework has been configured.
    rendered = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)
    print(rendered, flush=True)
    return rendered
