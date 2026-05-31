from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class LicenseCreate(BaseModel):
    license_number : str
    expiration_date : date
    state : str
    ce_hours_required : int
    
    
class LicenseResponse(BaseModel):
    id : int
    license_number : str
    expiration_date : date
    ce_hours_required : int
    ce_hours_completed : int
    created_at : datetime
    status : Optional[str] = None
    state : str
    
    class Config:
        from_attributes = True
        
class LicenseUpdate(BaseModel):
    license_number : Optional[str] = None
    expiration_date : Optional[date] = None
    ce_hours_required : Optional[int] = None
    status : Optional[str] = None
    state : Optional[str] = None