from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import pyotp

app = FastAPI()

# ✅ CORS configuration to allow browser-based fetch() from Dynatrace or any other frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/")
def read_root():
    return {"status": "OK", "message": "OTP service is running"}

# ✅ OTP generation using pyotp (HOTP)
@app.post("/generate-otp")
async def generate_otp(req: Request):
    try:
        data = await req.json()
        master_key = data.get("master_key")

        if not master_key:
            raise HTTPException(status_code=400, detail="Missing master_key")

        # Counter can be dynamic or constant. Use a constant for testing.
        counter = 0

        # Generate OTP using pyotp
        hotp = pyotp.HOTP(master_key)
        otp = hotp.at(counter)

        return {"otp": otp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
