from pwn import *
import hashlib, json
from datetime import datetime
from random import randrange
from Crypto.Util.number import bytes_to_long, inverse
from utils import json_recv, json_send
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192

def sha1(data):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(data)
        return sha1_hash.digest()

r = remote('socket.cryptohack.org', 13381)

g = generator_192
n = g.order()
welcome = json_recv(r)

list_signs = []
a_match = False
to_send = {
    'option': 'sign_time'
}

json_send(r, to_send)
signature = json.loads(json_recv(r).decode())
if 'erro' in signature.keys():
    raise 'Sorry restart'
list_signs.append(signature)
sign1 = {}
sign2 = {}
while not a_match:
    json_send(r, to_send)
    signature = json.loads(json_recv(r).decode())
    if 'erro' in signature.keys():
        raise 'Sorry restart'
    for sign in list_signs:
        if signature['r'] == sign['r']:
            sign1 = signature
            sign2 = sign 
            a_match = True
            break
    list_signs.append(signature)

# From sign1 and sign2 we can campute the secret
# in fact : secret = (s*k - message_hash)/r where k = (m1.hash - m2.hash)/(s1-s2)
m1hash = bytes_to_long(sha1(sign1['msg'].encode()))
m2hash = bytes_to_long(sha1(sign2['msg'].encode()))
s1 = int(sign1['s'],16)
s2 = int(sign2['s'],16)
r1 = int(sign1['r'],16)
r2 = int(sign2['r'],16)

p = generator_192.curve().p()
k = ((m1hash - m2hash)*inverse(s1-s2, n))%n
secret = ((s1*k - m1hash)*inverse(r1,n)) % n 

pubkey = Public_key(g, g * secret)
privkey = Private_key(pubkey, secret)

msg = 'unlock'
hsh = sha1(msg.encode())
sig = privkey.sign(bytes_to_long(hsh), randrange(1, g.order()))
to_send = {"option": "verify","msg": msg, "r": hex(sig.r), "s": hex(sig.s)}

json_send(r, to_send)

flag = json_recv(r).decode()
r.close()
print("flag is : ", flag)
