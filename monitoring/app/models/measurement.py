from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class Measurement(BaseModel):
    device_id: str
    timestamp: datetime
    payload: Dict
