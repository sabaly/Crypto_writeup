from pwn import *
import json
from utils import *

r = remote('socket.cryptohack.org', 13371)

received = json_recv(r)
received = json.loads(received[received.find(b'{'): received.find(b'}')+1].decode())

p = received['p']
g = received['g']
A = received['A']

# we send to bob our own parameters
to_send = {
    "p" : p,
    "g" : "0x02",
    "A" : "0x04"
}

json_send(r, to_send)

received = json_recv(r)
received = json.loads(received[received.find(b'{'): received.find(b'}')+1].decode())


# we send to Alice our own parameters
to_send = {
    "B" : "0x04"
}
json_send(r, to_send)

data = json_recv(r)
data = json.loads(data[data.find(b'{'): data.find(b'}')+1].decode())

shared_secret = pow(int(A, 16), 2, int(p,16))
iv = data['iv']
ciphertext = data['encrypted_flag']

flag = decrypt_flag(shared_secret, iv, ciphertext)
r.close()

print("flag is : ", flag)