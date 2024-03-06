from pwn import *
import json
from sage.all import *
from Crypto.Util.number import inverse

# dimension
n = 64
# plaintext modulus
p = 257
# ciphertext modulus
q = 0x10001

V = VectorSpace(GF(q), n)

r = remote('socket.cryptohack.org', 13411) # level = 'debug'

def json_recv():
    line = r.recvline()
    if b'{' not in line:
        return line
    return json.loads(line.decode())

def json_send(data):
    request = json.dumps(data).encode()
    r.sendline(request)

def list_int(L):
    L = L[1:len(L)-1]
    L = L.replace(' ', '')
    L = L.split(',')
    return [int(x) for x in L]
max = n
received = json_recv() # initiate connexion
print(received)
M = [None]*n
while max != 0:
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
    max -= 1
    
#K = V['x']
M = matrix(GF(q), M)
Kernel = M.right_kernel()
S = list(Kernel.basis()[0])
inv = inverse(S[-1], q)
S = [x*inv for x in S]
S = vector(S)
A = vector(A[:-1])
# check
assert b-A*S[:-1]==1
S = S[:-1]
print("Secrete S : ", S)
# Now we have s we can the Flag
flag = ""
ind = 0
while "}" not in flag:
    tosend = {
        "option": "get_flag",
        "index": str(ind)
    }
    json_send(tosend)
    rcv = json_recv()
    A = list_int(rcv['A'])
    b = int(rcv['b'])
    A = vector(A)
    flag += chr(b - A*S)
    ind += 1

print("flag is : ", flag)

