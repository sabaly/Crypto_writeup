""" 
    ct = m^16 [N] = (((m^2)^2)^2)^2 [N].

    we juste have to campute successive square roots t'il we find the good one. 

    I used PARI/GP to solve the problem. 

    In the brokenRSA.gp file is the PARI/GP code that camputes the squareroots. 
    I cannot convert long to bytes from PARI/GP so i have written the results in brookenRSA.txt.

    I read the results with the following python code et get the flag from one of this results.
"""
from Crypto.Util.number import long_to_bytes

with open('brokenRSA.txt', 'r') as f:
    results = f.readlines()

for x in results:
    tmp = long_to_bytes(int(x))
    if b'crypto' in tmp:
        print("flag is : ", tmp)
    