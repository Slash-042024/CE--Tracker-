from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.license_holder import LicenseHolder
from app.schemas.license_holder import LicenseHolderCreate,LicenseHolderResponse, LicenseHolderUpdate

router = APIRouter(prefix='/license-holders', tags=['license-holders'])

@router.get("/", response_model=list[LicenseHolderResponse])
def get_all(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(LicenseHolder).filter(LicenseHolder.user_id == current_user.id).all()

@router.get("/{license_holder_id}", response_model=LicenseHolderResponse)

def get_one(license_holder_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lh = db.query(LicenseHolder).filter(LicenseHolder.id == license_holder_id, LicenseHolder.user_id == current_user.id).first()
    if not lh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License holder not found")   
    return lh

@router.post("/", response_model=LicenseHolderResponse, status_code=status.HTTP_201_CREATED)

def create_one(data: LicenseHolderCreate, current_user: User =Depends(get_current_active_user), db: Session = Depends(get_db)):
    lh = LicenseHolder(user_id=current_user.id,
                       name=data.name,
                       email=data.email,
                       phone=data.phone,
                       trade=data.trade,
    )
    db.add(lh)
    db.commit()
    db.refresh(lh)
    return lh

@router.patch("/{license_holder_id}", response_model=LicenseHolderResponse)

def update_one(license_holder_id: int, data: LicenseHolderUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lh = db.query(LicenseHolder).filter(LicenseHolder.id == license_holder_id, LicenseHolder.user_id == current_user.id).first()
    if not lh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License holder not found")
    if data.name is not None:
        lh.name = data.name
    if data.email is not None:
        lh.email = data.email
    if data.phone is not None:
        lh.phone = data.phone
    if data.trade is not None:
        lh.trade = data.trade
    db.commit()
    db.refresh(lh)
    return lh

@router.delete("/{license_holder_id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_one(license_holder_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lh = db.query(LicenseHolder).filter(LicenseHolder.id == license_holder_id, LicenseHolder.user_id == current_user.id).first()
    if not lh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License holder not found")
    lh.is_active = False
    db.commit()
    
    