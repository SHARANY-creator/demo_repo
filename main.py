from fastapi import FastAPI, HTTPException
import subprocess
import sys
from encoding_tools import TheSoCalledGreatEncoder, GuessEncodingFailedException

app = FastAPI()

def GenOathKey(oath_key: str) -> str:
    try:
        # NOTE: You may need to update this path for Linux on Render
        s2_out = subprocess.check_output(
            [sys.executable, "C:\\Users\\sharany\\Setup_python\\oathtool", oath_key]
        )
        encoder = TheSoCalledGreatEncoder()
        encoder.load_bytes(s2_out)
        encoder.decode()
        return encoder.decoded_data.replace('\r\n', '')
    except GuessEncodingFailedException as e:
        raise ValueError('Failed to decode OTP') from e
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Error calling oathtool") from e

@app.post("/generate-otp")
async def generate_otp(master_key: str):
    try:
        otp = GenOathKey(master_key)
        return {"otp": otp}
    except ValueError as ve:
        print("ValueError:", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc()  # <== This will show the exact error in logs
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
