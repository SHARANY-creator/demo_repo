from fastapi import FastAPI, HTTPException
import subprocess
import sys
import traceback
from encoding_tools import TheSoCalledGreatEncoder, GuessEncodingFailedException

app = FastAPI()

# Health check/root endpoint
@app.get("/")
def read_root():
    return {"status": "OK", "message": "OTP service is running"}

# Function to generate OTP
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
        print("Encoding guess failed:", e)
        raise ValueError('Failed to decode OTP') from e
    except subprocess.CalledProcessError as e:
        print("Subprocess error:", e)
        raise HTTPException(status_code=500, detail="Error calling oathtool") from e

# OTP generation endpoint
@app.post("/generate-otp")
async def generate_otp(master_key: str):
    try:
        otp = GenOathKey(master_key)
        return {"otp": otp}
    except ValueError as ve:
        print("ValueError:", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("Unexpected error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Only needed for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
