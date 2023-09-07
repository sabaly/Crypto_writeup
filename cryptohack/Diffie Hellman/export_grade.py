from pwn import *
from utils import decrypt_flag, json_recv, json_send
import json
from sage.all import *

r = remote('socket.cryptohack.org', 13379)

received = json_recv(r)
received = json.loads(received[received.find(b'{'): received.find(b'}')+1].decode())

# chosen the weakess
supported = received["supported"][-1]
to_send = {"supported": [supported]}
# send them to Bob
json_send(r, to_send)

# get Bob answer that we can send directly to Alice
chosen = json_recv(r)
chosen = json.loads(chosen[chosen.find(b'{'): chosen.find(b'}')+1].decode())

# send it to Alice
json_send(r, chosen)

# See below the supported DH
print("chosen : ", chosen["chosen"])

# now Alice send the encryped flag
alice = json_recv(r)
alice = json.loads(alice[alice.find(b'{'): alice.find(b'}')+1].decode())
p = int(alice['p'],16)
g = int(alice['g'],16)
A = int(alice['A'], 16)

bob = json_recv(r)
bob = json.loads(bob[bob.find(b'{'): bob.find(b'}')+1].decode())
B = int(bob['B'],16)

data = json_recv(r)
data = json.loads(data[data.find(b'{'): data.find(b'}')+1].decode())
iv  = data['iv']
ciphertext = data['encrypted_flag']

# The chosen DH is weak we can use classic algorithm to campute the exponent
field = GF(p)
g = field(g)
A = field(A)
B = field(B)

b = discrete_log(B,g)

shared_secret = pow(A,b,p)
flag = decrypt_flag(shared_secret, iv, ciphertext)
r.close()

print("flag is : ", flag)



