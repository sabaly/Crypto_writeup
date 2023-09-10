from pwn import *
from utils import json_recv, json_send
from Crypto.Util.number import bytes_to_long
import json 

r = remote('socket.cryptohack.org', 13399)

received = json_recv(r)
passwd = b'00000000000000000000000000000'
# reset the password now
reset = {"option": "reset_password", "token": passwd.hex()}
json_send(r, reset)
received = json.loads(json_recv(r).decode())
if 'msg' in received.keys():
    if received['msg'] != 'Password has been correctly reset.':
        print('Error : ', received['msg'])
        exit(0)
# password was reset
authenticate = {"option": "authenticate", "password": ""}
ct = passwd[16:]
for c in range(2**8):
    token = bytes([x ^ c for x in ct])

    passwd_length = bytes_to_long(token[-4:])
    password = token[:-4][:passwd_length]
    try:
        authenticate["password"] = password.decode()
    except:
        continue
    
    json_send(r, authenticate)
    received = json.loads(json_recv(r).decode())
    if 'admin' in received['msg']:
        r.close()
        print(received['msg'])
        exit(0)