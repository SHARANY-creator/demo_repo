import pyotp


secret = 'BBMACJFO5HHNSAQXIRCECMLAYSUZIMIH'
totp = pyotp.TOTP(secret)

print("current OTP:", totp.now())