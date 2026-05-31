from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    account_type : str
    
class UserResponse(BaseModel):
    id : int
    name : str
    email : str
    phone : Optional[str] = None
    account_type : str
    is_active : bool
    created_at : datetime
    
    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    
   