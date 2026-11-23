from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditLogModel:
    id: str
    action: str
    actor_id: str
    resource_type: str
    timestamp: datetime
    ip_address: str
