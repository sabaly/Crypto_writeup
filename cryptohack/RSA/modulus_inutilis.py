""" 
e = 3 (very small) and p,q are 1024 bits so N is huge

Probably pt**3 is very very small compare to N then ct  is the cubic of pt in integer.
We thus have to compute the cubic root of ct over integers.

with pari/gp we just have : pt = ct^(1/3)
"""
from Crypto.Util.number import long_to_bytes

ct = 243251053617903760309941844835411292373350655973075480264001352919865180151222189820473358411037759381328642957324889519192337152355302808400638052620580409813222660643570085177957
# with pari/gp : pt = ct^(1/3)
pt = 624239975241694158443315202759206900318542905782320965248893

assert pt**3 == ct
print("flag is : ", long_to_bytes(pt))

