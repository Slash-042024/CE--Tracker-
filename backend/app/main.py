from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.models import user, license_holder, license, ce_course, alert_log, subscription
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.license_holders import router as license_holders_router
from app.routers.licenses import router as licenses_router


app = FastAPI(
    title = "CE Tracker API",
    description = "Continuing Education Tracker for licensed Tradespeople",
    version = "1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(license_holders_router)
app.include_router(licenses_router)

@app.get("/")
def root():
    return {"message": " CE Tracker API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}



