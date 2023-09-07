from pwn import *
import json
from utils import decrypt_flag, json_recv, json_send

r = remote('socket.cryptohack.org', 13373)

alice = json_recv(r)
alice = json.loads(alice[alice.find(b'{'): alice.find(b'}')+1].decode())
p = int(alice['p'], 16)
g = int(alice['g'], 16)
A = alice['A']

bob = json_recv(r)

data = json_recv(r)
data = json.loads(data[data.find(b'{'): data.find(b'}')+1].decode())
iv = data['iv']
ciphertext = data['encrypted']

# Bob uses the same secret when we send him data, he's the static clien
# so we juste have to send him A as g to have there shared_secret
to_send = {
    "p": alice['p'],
    "g": A,
    "A": "0x01"
}
json_send(r, to_send)
secret = json_recv(r)
secret = json.loads(secret[secret.find(b'{'): secret.find(b'}')+1].decode())
shared_secret = int(secret['B'],16)

flag = decrypt_flag(shared_secret, iv, ciphertext)
r.close()

print("flag is : ", flag)

