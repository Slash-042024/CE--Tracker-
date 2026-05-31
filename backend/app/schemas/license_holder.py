from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LicenseHolderCreate(BaseModel):
    name : str
    email : str
    phone : Optional[str] = None
    trade : str
  
    
class LicenseHolderResponse(BaseModel):
    id : int
    name : str
    email : str
    phone : Optional[str] = None
    trade : str
    created_at : datetime
    is_active : bool
     
    class Config:
        from_attributes = True
        
class LicenseHolderUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None
    phone : Optional[str] = None
    trade : Optional[str] = None
    
    