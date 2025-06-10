from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pyotp
import traceback

app = FastAPI()

# ✅ CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Change to your Dynatrace domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check endpoint
@app.get("/")
def root():
    return {"status": "OK", "message": "OTP service is running"}

# ✅ Request model
class OTPRequest(BaseModel):
    master_key: str = Field(..., min_length=16, description="Base32 encoded TOTP master key")

# ✅ OTP generation endpoint
@app.post("/generate-otp")
async def generate_otp(req: OTPRequest):
    try:
        if not req.master_key.isalnum():
            raise HTTPException(status_code=400, detail="master_key must be alphanumeric")
        
        totp = pyotp.TOTP(req.master_key)
        otp = totp.now()
        return {"otp": otp}

    except HTTPException as he:
        raise he
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate OTP due to server error")
