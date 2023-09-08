""" 
E: Y2 = X3 + 497 X + 1768, p: 9739, G: (1804,5368) 

We just have to campute q_y and the get the secret key = nb * (q_x,q_y)
"""
from utils import scal_mult, decrypt_flag
p = 9739
qx = 4726
nB = 6534
iv = 'cd9da9f1c60925922377ea952afc212c'
encrypted_flag =  'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

# campute y**2 from there get a square root 
ysquared = (qx**3 + 497*qx + 1768) % p

# since p = -1 [4], we have an easy square root
qy = ysquared ** ((p+1)//4) % p

assert qy**2 % p == (qx**3 + 497*qx + 1768) % p
A = [qx,qy]
key = scal_mult(nB, A, [497, 1768, p])

shared_secret = key[0]

print('flag is : ', decrypt_flag(shared_secret, iv, encrypted_flag))
