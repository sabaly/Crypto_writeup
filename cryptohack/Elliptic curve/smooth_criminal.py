from sage.all import GF, EllipticCurve, discrete_log
from utils import decrypt_flag
"""  
Parameters are very small so we can try attaque the discret log to find n.
"""
# Define the curve
p = 310717010502520989590157367261876774703
a = 2
b = 3

field = GF(p)
EC = EllipticCurve(field, [a,b])

public = EC(280810182131414898730378982766101210916,291506490768054478159835604632710368904)
G = EC(179210853392303317793440285562762725654,105268671499942631758568591033409611165)
B = EC(272640099140026426377756188075937988094,51062462309521034358726608268084433317)

n = discrete_log(B,G,G.order(),operation='+')

S = n*public
shared_secret = S[0]

iv = '07e2628b590095a5e332d397b8a59aa7'
encrypted_flag = '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'

print('flag is : ', decrypt_flag(shared_secret, iv, encrypted_flag))