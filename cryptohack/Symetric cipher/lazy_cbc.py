import requests

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

domain = 'https://aes.cryptohack.org/lazy_cbc/'

# Let's send the following message to decrypt : b'crypto{my__flag}crypto{my__flag}'
# We will get and Invalid plaintext and received the decrypted data. Interresting :)
fake_ciphertext = b'crypto{my__flag}crypto{my__flag}'.hex()
url = domain + f'/receive/{fake_ciphertext}/'
response = requests.get(url)
data = response.json()['error']

decrypted = data.split(':')[1]
# decrypted is a 32 bytes the first bloc of 16 is : b1 = xor(KEY, D(x))
# and the second one is : b2 = xor(D(x), x)
# where x is b'crypto{my__flag}'
# we can deduce the KEY witch is : KEY = xor(D(x), b1)
# let's goooo
decrypted = decrypted.strip() # delete space 
b1 = decrypted[:32]
b2 = decrypted[32:]

d_x = int(b2,16)^int(b'crypto{my__flag}'.hex(), 16)
key = int(b1,16)^d_x
key = hex(key)[2:]

# now we can send the key
url = domain + f'/get_flag/{key}/'
response = requests.get(url)
data = response.json()

flag = bytes.fromhex(data['plaintext'])

print('flag is : ', flag)

