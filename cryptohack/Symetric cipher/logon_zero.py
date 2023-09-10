from pwn import *
from utils import json_recv, json_send
from Crypto.Util.number import bytes_to_long
import json 

""" 
The weakness we exploite here is the decrypt function. So we choose the token such that the state will always remaine the same
by the way the b value. That's why we'll send as token : b'00000000000000000000000000000'

Then we can calcul ourself the same value of the decrypt function and then recover the new password.
"""

r = remote('socket.cryptohack.org', 13399)

received = json_recv(r)
passwd = b'00000000000000000000000000000'
# reset the password now
reset = {"option": "reset_password", "token": passwd.hex()}
json_send(r, reset) # reset the password
received = json.loads(json_recv(r).decode())
if 'msg' in received.keys():
    if received['msg'] != 'Password has been correctly reset.':
        print('Error : ', received['msg'])
        exit(0)
# password was reset
authenticate = {"option": "authenticate", "password": ""}
# now let's recover the new_password our self
ct = passwd[16:]
for c in range(2**8): # with > 50% chance the b value is here 
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
r.close()
print("Don't worry just restart it, you'll get the flag :-)")
print("(it's just because this time b value is not in [0, 255])")