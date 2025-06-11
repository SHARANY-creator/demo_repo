from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pyotp
import traceback

app = FastAPI()

# CORS Middleware to handle OPTIONS preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        # Log that the endpoint was hit
        print("OTP generation request received")

        # Validate master_key format
        if not req.master_key.isalnum():
            raise HTTPException(status_code=400, detail="master_key must be alphanumeric")

        # Generate OTP using pyotp
        totp = pyotp.TOTP(req.master_key)
        otp = totp.now()
        print(f"Generated OTP: {otp}")
        return {"otp": otp}

    except HTTPException as he:
        raise he  # Pass through FastAPI-style errors
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate OTP due to server error")
