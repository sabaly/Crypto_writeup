import requests 

domain = 'https://aes.cryptohack.org/'
def get_encrypted_flag():
    url = domain + '/ecbcbcwtf/encrypt_flag/'

    response = requests.get(url)

    return response.json()

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
# + means concat
# encrypted data = iv +E(iv^pt1) + E(ct1^pt2) where ct1 = E(iv^pt1)
enc = get_encrypted_flag()

iv = bytes.fromhex(enc['ciphertext'][:32])

ct = enc['ciphertext']

# decrypted data are : D(iv) + D(iv ^ pt1) + D(ct1 ^ pt2)
# and flag is pt1+pt2 we can get them as fallow : 
# pt1 = iv ^ D(iv ^ pt1) and pt2 = ct1 ^ D(ct1 ^ pt2)
url = domain + f'/ecbcbcwtf/decrypt/{ct}'
response = requests.get(url)

pt = response.json()

d_ct1 = bytes.fromhex(pt['plaintext'][32:64])

flag1 = byte_xor(d_ct1, iv)

d_ct2 = bytes.fromhex(pt['plaintext'][64:])

ct1 = bytes.fromhex(enc['ciphertext'][32:64])
flag2 = byte_xor(ct1, d_ct2)

print(flag1+flag2)

