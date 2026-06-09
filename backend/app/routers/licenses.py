from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.license import License
from app.models.license_holder import LicenseHolder
from app.schemas.license import LicenseCreate, LicenseResponse, LicenseUpdate

router = APIRouter(prefix='/licenses', tags=['licenses'])

@router.get("/", response_model=list[LicenseResponse])
def get_all(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(License).join(LicenseHolder).filter(
    LicenseHolder.user_id == current_user.id
).all()
@router.get("/{license_id}", response_model=LicenseResponse)
def get_one(license_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lic = db.query(License).join(LicenseHolder).filter(License.id == license_id, LicenseHolder.user_id == current_user.id).first()
    if not lic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    return lic

@router.post("/", response_model=LicenseResponse, status_code=201)
def create_one(data: LicenseCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lh = db.query(LicenseHolder).filter(LicenseHolder.id == data.license_holder_id, LicenseHolder.user_id == current_user.id).first()
    if not lh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License holder not found")
    lic = License(
         license_holder_id=data.license_holder_id,
         license_number=data.license_number,
         license_type=data.license_type,
         issuing_authority=data.issuing_authority,
         expiration_date=data.expiration_date,
         ce_hours_required=data.ce_hours_required,
  )
    db.add(lic)
    db.commit()
    db.refresh(lic)
    return lic

@router.patch("/{license_id}", response_model=LicenseResponse)
def update_one(license_id: int, data: LicenseUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lic = db.query(License).join(LicenseHolder).filter(License.id == license_id, LicenseHolder.user_id == current_user.id).first()
    if not lic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    if data.license_holder_id is not None:
        lh = db.query(LicenseHolder).filter(LicenseHolder.id == data.license_holder_id, LicenseHolder.user_id == current_user.id).first()
        if not lh:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License holder not found")
        lic.license_holder_id = data.license_holder_id
    if data.license_number is not None:
        lic.license_number = data.license_number
    if data.license_type is not None:
        lic.license_type = data.license_type
    if data.expiration_date is not None:
        lic.expiration_date = data.expiration_date
    if data.ce_hours_required is not None:
        lic.ce_hours_required = data.ce_hours_required
    if data.issuing_authority is not None:
        lic.issuing_authority = data.issuing_authority
    db.commit()
    db.refresh(lic)
    return lic

@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(license_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lic = db.query(License).join(LicenseHolder).filter(License.id == license_id, LicenseHolder.user_id == current_user.id).first()
    if not lic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    lic.is_active = False
    db.commit()
    