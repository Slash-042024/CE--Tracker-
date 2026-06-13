from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class CECourseCreate(BaseModel):
    license_id: int
    course_name: str
    hours_earned: int
    date_completed: date
    course_provider: str
    
class CECourseResponse(BaseModel):
    id : int
    course_name : str
    date_completed : date
    certificate_url : Optional[str] = None
    course_provider :str 
    created_at : datetime
    hours_earned : int
    
    class Config:
        from_attributes = True
        
        
class CECourseUpdate(BaseModel):
    course_name : Optional[str] = None
    date_completed : Optional[date] = None
    certificate_url : Optional[str] = None