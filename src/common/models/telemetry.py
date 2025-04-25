from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Optional
import json

@dataclass
class TelemetryData:
    sensor_id: str
    timestamp: datetime
    value: Any
    metadata: Optional[dict] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ControlCommand:
    device_id: str
    command: str
    parameters: Optional[dict] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
