from pwn import *
import fastecdsa, json
from fastecdsa.point import Point
from Crypto.Util.number import inverse
from utils import json_recv, json_send

r = remote("socket.cryptohack.org", 13382)

q = fastecdsa.curve.P256.q
G = fastecdsa.curve.P256.G
assert G.x, G.y == [0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
                    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5]

public = Point(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)

d = 2
d_inv = inverse(d,q)

fake_gen = d_inv*public
assert d*fake_gen == public
to_send = {
    'private_key': d,
    'host': 'www.bing.com',
    'curve' : '',
    'generator': [fake_gen.x, fake_gen.y]
}

received = json_recv(r)
json_send(r, to_send)

data = json_recv(r).decode()
flag = (data[data.find('crypto'): data.find('}')+1])
r.close()

print("flag is : ", flag)
