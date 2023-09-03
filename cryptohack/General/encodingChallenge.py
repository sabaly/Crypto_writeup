from pwn import * # pip install pwntools
import json
import base64
import codecs 
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def solution(type, encoded):
    if type == 'hex':
        data = bytes.fromhex(encoded).decode('utf8')
    elif type == 'base64':
        data = base64.b64decode(encoded).decode('utf8')
    elif type == 'rot13':
        data = codecs.decode(encoded, 'rot_13')
    elif type == 'bigint':
        encoded = int(encoded, 16)
        data = long_to_bytes(encoded).decode('utf8')
    elif type == 'utf-8':
        data = ''.join([chr(x) for x in encoded])
    return data

received = {}

while error not in received.keys():
    received = json_recv()

    print("Received type: ")
    type = received["type"]
    print("Received encoded value: ")
    encoded = received["encoded"]



    to_send = {
        "decoded": str(solution(type, encoded))
    }
    json_send(to_send)
    

