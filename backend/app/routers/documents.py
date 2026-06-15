from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.license import License
from app.models.license_holder import LicenseHolder
from app.models.ce_course import CECourse
from app.services.s3_service import upload_file, generate_presigned_url

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/{license_id}/{course_id}")
def upload_documents(
    license_id: int,
    course_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    lic = db.query(License).join(LicenseHolder).filter(
        License.id == license_id,
        LicenseHolder.user_id == current_user.id
    ).first()
    if not lic:
        raise HTTPException(status_code=403, detail="License not found")
    course = db.query(CECourse).filter(
        CECourse.id == course_id,
        CECourse.license_id == license_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    folder = f"users/{current_user.id}/licenses/{license_id}"
    key = upload_file(file.file, folder, file.filename)
    
    url = generate_presigned_url(key)
    course.certificate_url = key
    db.commit()
    return {
        "message": "Certificate uploaded successfully",
        "certificate_url": url,
        "key": key
    }
    
@router.get("/{license_id}")
def get_documents(
    license_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lic = db.query(License).join(LicenseHolder).filter(
        License.id == license_id,
        LicenseHolder.user_id == current_user.id
    ).first()
    if not lic:
        raise HTTPException(status_code=403, detail="License not found")
    
    courses = db.query(CECourse).filter(
        CECourse.license_id == license_id,
        CECourse.certificate_url != None
    ).all()
    
    result = []
    for course in courses:
        result.append({
            "course_id": course.id,
            "course_name": course.course_name,
            "date_completed": str(course.date_completed),
            "certificate_url": generate_presigned_url(course.certificate_url)
        })
    return result