from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
import requests

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
cookie = f"admin=False;expiry={expires_at}".encode()
padded = pad(cookie,16).hex()

second_bloc = bytes.fromhex(padded[:32])
# will replace first bloc
replace_first_bloc = byte_xor(second_bloc, b';admin=True;0000;')


# get cookie 
url = 'https://aes.cryptohack.org/flipping_cookie/get_cookie/'
cookie = requests.get(url).json()['cookie']
iv = bytes.fromhex(cookie[:32])

replace_first_bloc = byte_xor(iv, replace_first_bloc)

new_cookie = replace_first_bloc + bytes.fromhex(cookie[32:])

url = f'https://aes.cryptohack.org/flipping_cookie/check_admin/{new_cookie.hex()}/{iv.hex()}/'
response = requests.get(url)

data = response.json()
print(data)
