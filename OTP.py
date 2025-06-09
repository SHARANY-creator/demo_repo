from builtins import ValueError
import subprocess
import sys
from os import replace
from encoding_tools import TheSoCalledGreatEncoder, GuessEncodingFailedException




def GenOathKey(oath_key):
    s2_out = subprocess.check_output(
        [sys.executable, "C:\\Users\\sharany\\Setup_python\\oathtool", oath_key])
    # s2_out = subprocess.check_output([sys.executable, "/usr/local/lib/python3.8/oathtool", oath_key])

    encoder = TheSoCalledGreatEncoder()
    encoder.load_bytes(s2_out)
    try:
        encoder.decode()
        decoded_string = encoder.decoded_data
        decoded_string = decoded_string.replace('\r\n', '')

    except GuessEncodingFailedException as e:
        raise ValueError('Wrong input...')(e)
    return decoded_string


master_key = "SZJLKA2HXHVXALFD72OOFHJNZBKOVNGO"  # For : TE02929
ver_code = GenOathKey(master_key)
print(ver_code)