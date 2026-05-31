from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class AlertLogResponse(BaseModel):
    id : int
    license_id : int
    alert_method : str
    sent_to : str
    days_remaining : int
    status : str
    sent_at : datetime
    
    class Config:
        from_attributes = True