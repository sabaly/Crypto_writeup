# import the gaussian reduction function
from gaussian_reduction import GR, normVec
from Crypto.Util.number import long_to_bytes, inverse

""" 
    We can deduce from h = inverse(f,q)*g [q] that the lattice is genrated by (h,1), (q,1) cause we can observe that : (g, f-k) = f*(h,1) - k * (q,1)
    with some integer k.
    As g is small and so does f-k so (g, f-k) is a small vector of that lattice. So gausse reduction may give us 
    this vector.
"""
# the decrypt function
def decrypt(q, f, g, e):
    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return long_to_bytes(m)

q,h = (7638232120454925879231554234011842347641017888219021175304217358715878636183252433454896490677496516149889316745664606749499241420160898019203925115292257, 2163268902194560093843693572170199707501787797497998463462129592239973581462651622978282637513865274199374452805292639586264791317439029535926401109074800)
enc_flag = 5605696495253720664142881956908624307570671858477482119657436163663663844731169035682344974286379049123733356009125671924280312532755241162267269123486523

v1 = (h,1)
v2 = (q,1)

u,v = GR(v1,v2)

if normVec(u) < normVec(v):
    g = u[0]
else:
    g = v[0]
# f 
f = inverse(h,q)*g % q
print(decrypt(q,f,g,enc_flag))


