from pydantic import AnyUrl, BaseModel
from typing import Optional, Dict, Any


class CeleryConfig(BaseModel):
    broker: AnyUrl
    backend: AnyUrl
    result_expires: Optional[int] = None
    broker_connection_retry_on_startup: Optional[bool] = None
    result_backend_transport_options: Optional[Dict[str, Any]] = None
