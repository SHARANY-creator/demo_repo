from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import sys
from encoding_tools import TheSoCalledGreatEncoder, GuessEncodingFailedException

app = FastAPI()

# Add a root endpoint so / doesn't give 404
@app.get("/")
def read_root():
    return {"status": "OK", "message": "OTP service is running"}

# Request model for POST body
class OTPRequest(BaseModel):
    master_key: str

# Core OTP generation logic
def GenOathKey(oath_key: str) -> str:
    try:
        # Call oathtool (adjust path if needed)
        s2_out = subprocess.check_output(
            [sys.executable, "C:\\Users\\sharany\\Setup_python\\oathtool", oath_key]
        )
        # Decode the output using your custom encoder
        encoder = TheSoCalledGreatEncoder()
        encoder.load_bytes(s2_out)
        encoder.decode()
        return encoder.decoded_data.replace('\r\n', '')
    except GuessEncodingFailedException as e:
        raise ValueError('Failed to decode OTP') from e
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Error calling oathtool") from e

# OTP generation API endpoint
@app.post("/generate-otp")
async def generate_otp(req: OTPRequest):
    try:
        otp = GenOathKey(req.master_key)
        return {"otp": otp}
    except ValueError as ve:
        print("ValueError:", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc()  # Full error traceback
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run locally (Render ignores this, but useful for local dev)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
