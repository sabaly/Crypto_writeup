from math import gcd
from sympy.ntheory import primefactors

# 588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237
# x = 114x - 113x = 851 - 642  = 209 [p] can take x=209

n = gcd(114*209 - 851, 113*209 - 642)

# gives p
print(primefactors(n))
