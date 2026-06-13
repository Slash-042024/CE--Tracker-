from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.ce_course import CECourse
from app.models.license import License
from app.models.license_holder import LicenseHolder
from app.schemas.ce_course import CECourseCreate, CECourseResponse, CECourseUpdate

router = APIRouter(prefix="/ce-courses", tags=["CE Courses"])

@router.post("/", response_model=CECourseResponse, status_code=status.HTTP_201_CREATED)
def create_ce_course(
    ce_course_in: CECourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    lic = db.query(License).join(LicenseHolder).filter(License.id == ce_course_in.license_id, LicenseHolder.user_id == current_user.id).first()
    if not lic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    lic_course = CECourse(
        license_id=ce_course_in.license_id,
        license_holder_id=ce_course_in.license_holder_id,
        course_name=ce_course_in.course_name,
        provider=ce_course_in.provider,
        completion_date=ce_course_in.completion_date,
        ce_hours=ce_course_in.ce_hours
    )
    lic.ce_hours_completed += ce_course_in.ce_hours
    db.add(lic_course)
    db.commit()
    db.refresh(lic_course)
    return lic_course

@router.get("/{course_id}", response_model=CECourseResponse)

def get_ce_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ce_course = db.query(CECourse).join(LicenseHolder).filter(CECourse.id == course_id, LicenseHolder.user_id == current_user.id).first()
    if not ce_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CE Course not found")
    return ce_course

@router.get("/", response_model=list[CECourseResponse])
def read_ce_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(CECourse).join(LicenseHolder).filter(LicenseHolder.user_id == current_user.id).all()

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ce_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ce_course = db.query(CECourse).join(LicenseHolder).filter(CECourse.id == course_id, LicenseHolder.user_id == current_user.id).first()
    if not ce_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CE Course not found")
    if not ce_course.is_active:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CE Course not found")
    lic = db.query(License).join(LicenseHolder).filter(License.id == ce_course.license_id, LicenseHolder.user_id == current_user.id).first()
    if lic:
        lic.ce_hours_completed -= ce_course.ce_hours
    ce_course.is_active = False
    db.commit()