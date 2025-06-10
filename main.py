from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pyotp
import traceback

app = FastAPI()

# Health check endpoint
@app.get("/")
def root():
    return {"status": "OK", "message": "OTP service is running"}

# Request model with validation
class OTPRequest(BaseModel):
    master_key: str = Field(..., min_length=16, description="Base32 encoded TOTP master key")

# OTP generation endpoint
@app.post("/generate-otp")
async def generate_otp(req: OTPRequest):
    try:
        # Validate master_key format
        if not req.master_key.isalnum():
            raise HTTPException(status_code=400, detail="master_key must be alphanumeric")

        # Generate OTP
        totp = pyotp.TOTP(req.master_key)
        otp = totp.now()
        return {"otp": otp}

    except HTTPException as he:
        raise he  # Let FastAPI handle known exceptions
    except Exception as e:
        # Log unexpected errors for debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate OTP due to server error")
