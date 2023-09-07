from pwn import *
import json
from utils import decrypt_flag, json_recv, json_send
from sage.all import *

r = remote('socket.cryptohack.org', 13380)

""" 
Just compute aG*bG = abG^2, the share secret is abG^2/G
"""

alice = json_recv(r)
alice = json.loads(alice[alice.find(b'{'): alice.find(b'}')+1].decode())
p = int(alice['p'], 16)
g = int(alice['g'], 16)
A = int(alice['A'], 16)

bob = json_recv(r)
bob = json.loads(bob[bob.find(b'{'): bob.find(b'}')+1].decode())
B = int(bob['B'],16)

data = json_recv(r)
data = json.loads(data[data.find(b'{'): data.find(b'}')+1].decode())
iv = data['iv']
ciphertext = data['encrypted']

field = GF(p)
shared_secret = field(A)*field(B)/2

flag = decrypt_flag(shared_secret, iv, ciphertext)
r.close()

print("flag is : ", flag)