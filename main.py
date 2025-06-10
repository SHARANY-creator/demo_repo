from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import sys
from encoding_tools import TheSoCalledGreatEncoder, GuessEncodingFailedException

app = FastAPI()

class OTPRequest(BaseModel):
    master_key: str

def GenOathKey(oath_key: str) -> str:
    try:
        s2_out = subprocess.check_output(
            [sys.executable, "C:\\Users\\sharany\\Setup_python\\oathtool", oath_key]
        )
        encoder = TheSoCalledGreatEncoder()
        encoder.load_bytes(s2_out)
        encoder.decode()
        return encoder.decoded_data.replace('\r\n', '')
    except GuessEncodingFailedException as e:
        raise ValueError('Failed to decode OTP') from e
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Error calling oathtool")

@app.post("/generate-otp")
async def generate_otp(payload: OTPRequest):
    try:
        otp = GenOathKey(payload.master_key)
        return {"otp": otp}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
