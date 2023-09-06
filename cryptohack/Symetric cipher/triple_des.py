import requests
from Crypto.Util.Padding import unpad
""" 
To solve this challenge, One have to know how 3DES works. Let's do it easy here
ct = E(D(E(pt, k1), k2), k3)
ct: ciphertext and pt: plaintext
k1, k2 and k3 are three (différents!) keys. The middle function is a décryption one.

THE WEAKNESS is due to some specific keys called weak keys :-).
details herer in wiki : https://en.wikipedia.org/wiki/Weak_key#Weak_keys_in_DES
"""

# now it's easy te get the flag
key = '0101010101010101FEFEFEFEFEFEFEFE' # is a weak key

domain = 'https://aes.cryptohack.org/triple_des/'

url = domain + f'/encrypt_flag/{key}/'

enc_flag = requests.get(url).json()['ciphertext']

# getting the flag
url = domain + f'/encrypt/{key}/{enc_flag}/'
flag = requests.get(url).json()['ciphertext']

flag = unpad(bytes.fromhex(flag), 8)

print('flag is : ', flag)
