from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import inverse
import hashlib
from math import floor
import json

def point_addition(P,Q,E):
    if len(E) < 3:
        raise 'invalid curve parameters'
    if P == []:
        return Q 
    elif Q == []:
        return P 
    
    if P[0]==Q[0] and P[1] == - Q[1]:
        return []
    if P != Q:
        lmbda = ((Q[1] - P[1]) * inverse(Q[0] - P[0], E[2])) % E[2]
    else:
        lmbda = ((3*P[0]**2 + E[0])*inverse(2*P[1], E[2])) % E[2]
    x = (lmbda**2 - P[0] - Q[0]) % E[2]
    y = (lmbda*(P[0] - x) - P[1]) % E[2]

    return x,y

def scal_mult(n, G, E):
    if n < 1 or len(E) < 3:
        raise 'parameters error'
    P = G 
    R = []
    while n>0:
        if n%2 == 1:
            R = point_addition(R,P,E)
        P = point_addition(P,P,E)
        n = floor(n/2)
    return R

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


def json_recv(r):
    line = r.recvline()
    if b'{'!=line[0] or b'}'!=line[-1]:
        return line
    return json.loads(line.decode())

def json_send(r, hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
    
