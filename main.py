from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pyotp
import os
import time
import logging
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
#app.add_middleware(
    #CORSMiddleware,
    #allow_origins=["*"],  # You can restrict this in production
    #allow_credentials=True,
    #allow_methods=["*"],
    #allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Secure master key (shared secret for OTP generation)
MASTER_KEY = os.getenv("MASTER_KEY", "SZJLKA2HXHVXALFD72OOFHJNZBKOVNGO")

class OTPRequest(BaseModel):
    master_key: str

@app.post("/generate-otp")
async def generate_otp(request: OTPRequest):
    if request.master_key != MASTER_KEY:
        logging.warning("Invalid master key attempt")
        return {"error": "Unauthorized"}, 401

    logging.info("OTP generation request received")

    # Wait for the OTP input field to be available (max 10s)
    totp = pyotp.TOTP(MASTER_KEY)
    otp = totp.now()

    logging.info(f"Generated OTP: {otp}")
    return {"otp": otp}
