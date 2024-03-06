

# This file was *autogenerated* from the file noise_free.sage
from sage.all_cmdline import *   # import sage library

_sage_const_64 = Integer(64); _sage_const_257 = Integer(257); _sage_const_0x10001 = Integer(0x10001); _sage_const_13411 = Integer(13411); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0)
from pwn import *
import json
#from sage.all import *

# dimension
n = _sage_const_64 
# plaintext modulus
p = _sage_const_257 
# ciphertext modulus
q = _sage_const_0x10001 

V = VectorSpace(GF(q), n)

r = remote('socket.cryptohack.org', _sage_const_13411 ) # level = 'debug'

def json_recv():
    line = r.recvline()
    if b'{' not in line:
        return line
    return json.loads(line.decode())

def json_send(data):
    request = json.dumps(data).encode()
    r.sendline(request)

def list_int(L):
    L = L[_sage_const_1 :len(L)-_sage_const_1 ]
    L = L.replace(' ', '')
    L = L.split(',')
    return [int(x) for x in L]
max = n
received = json_recv() # first read data
print(received)
M = [None]*n
while max != _sage_const_0 :
    tosend = {
        "option": "encrypt",
        "message": str(max)
    }
    json_send(tosend)
    rcv = json_recv()
    A = list_int(rcv['A'])
    b = int(rcv['b'])
    A.append(max - b)
    M[n-max] = A
    max -= _sage_const_1 
    
K = V['x']; (x,) = K._first_ngens(1)
M = matrix(K, M)
Kernel = M.right_kernel()
S = vector(list(Kernel.basis()[_sage_const_0 ]))
print("S = ", S)
A = vector(A)
print("Check : ", A*S - b)

