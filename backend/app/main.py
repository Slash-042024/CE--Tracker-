from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI(
    title = "CE Tracker API",
    description = "Continuing Education Tracker for licensed Tradespeople",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://Localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.get("/")
def root():
    return {"message": " CE Tracker API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}
