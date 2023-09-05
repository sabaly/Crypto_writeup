from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests

def show_bytes(data):
    for x in range(0,len(data), 32):
        print(data[x:x+32], ' ')

domain = 'https://aes.cryptohack.org/ecb_oracle/encrypt/'

prefix = 'AA'

response = requests.get(domain+prefix)

data = response.json()['ciphertext']
length = len(data)
n = 1
tmp = length

while tmp == length:
    prefix += 'AA'
    n+=1
    response = requests.get(domain+prefix)

    data = response.json()['ciphertext']
    length = len(data)
""" 
We find n = 7.

From this observation we can obtain the flag's length in fact we have :
data = \AA\AA...\AA + flag + new_padding_block 
where \AA\AA...\AA  is n bytes et new_padding_block is 16 bytes block
Since data is composed of 3 four 16 blocks (show_bytes(data)) the first one is : \AA...\AA + flag_part1
the second is : flag_part2 which is a 16 bytes block
the last is the new_padding_block

So flag is of length 25.
"""
""" prefix = 'AA'*38
print(prefix)
response = requests.get(domain+prefix)
data = response.json()['ciphertext']
show_bytes(data) """
# start the attack now
m = 31
flag = ''
while len(flag) < 25:
    prefix = 'AA'*m
    url = domain + prefix
    response = requests.get(url)
    data = response.json()['ciphertext']
    bloc = data[32:64]
    for c in range(33,127):
        url = domain + 'AA'*m + flag.encode().hex() + chr(c).encode().hex()
        response = requests.get(url)
        data = response.json()['ciphertext']

        if bloc == data[32:64]:
            print('found : ', chr(c))
            flag+=chr(c)
            break 
    m -= 1
print('flag is : ', flag)