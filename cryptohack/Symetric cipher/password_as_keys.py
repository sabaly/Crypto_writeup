import requests
import hashlib
from Crypto.Cipher import AES

domain = 'https://aes.cryptohack.org/passwords_as_keys/'
def get_encrypted_flag():
    url = domain+'/encrypt_flag/'

    response = requests.get(url)

    return response.json()

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}
# we are doing a dictionnary attack
with open('words') as f:
    words = [w.strip() for w in f.readlines()]

enc_flag = get_encrypted_flag()['ciphertext']

print('En cours...')
for password in words:
    KEY = hashlib.md5(password.encode()).digest()
    
    
    data = decrypt(enc_flag, KEY.hex())
    
    if b'crypto' in bytes.fromhex(data['plaintext']):
        print('password : ', password)
        print('flag : ', bytes.fromhex(data['plaintext']))
        break
    
    url = domain + f'/decrypt/{enc_flag}'
