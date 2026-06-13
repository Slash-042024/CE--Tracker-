from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.license import License
from app.models.license_holder import LicenseHolder

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")

def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    today = date.today()
    
    licenses = db.query(License).join(LicenseHolder).filter(
        LicenseHolder.user_id == current_user.id, License.is_active == True
        ).all()
    
    result = []
    for lic in licenses:
        days_remaining = (lic.expiration_date - today).days
        if days_remaining <=7:
            alert_status ="red"
        elif days_remaining <= 30:
            alert_status = "orange"
        elif days_remaining <= 60:
            alert_status = "yellow"
        else:
            alert_status = "green"
            
        result.append({
            "license_id": lic.id,
            "license_number": lic.license_number,
            "license_type": lic.license_type,
            "expiration_date": str(lic.expiration_date),
            "days_remaining": days_remaining,
            "ce_hours_completed": lic.ce_hours_completed,
            "ce_hours_required": lic.ce_hours_required,
            "alert_status": alert_status
            })
    
    return {
        "total_licenses": len(licenses),
        "red": len([r for r in result if r["alert_status"] == "red"]),
        "orange": len([r for r in result if r["alert_status"] == "orange"]),
        "yellow": len([r for r in result if r["alert_status"] == "yellow"]),
        "green": len([r for r in result if r["alert_status"] == "green"]),
        "license": result
    }