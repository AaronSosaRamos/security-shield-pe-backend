from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class MessageZoneChat(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    department: str
    province: str
    district: str
    fullname: str
    message_content: str
    order: int 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_alert: bool
