from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyotp

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Body Schema
class OTPRequest(BaseModel):
    master_key: str

@app.post("/generate-otp")
def generate_otp(request: OTPRequest):
    try:
        totp = pyotp.TOTP(request.master_key)
        otp = totp.now()
        return {"otp": otp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
