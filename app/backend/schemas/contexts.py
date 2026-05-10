from dataclasses import dataclass
from typing import Any, Dict

# dataclasses: just a structure in memory
@dataclass
class RequestContext:
    request_id: str
    client_ip: str | None
    headers: Dict[str, Any]
    query_params: Dict[str, Any]
    raw_body: bytes
