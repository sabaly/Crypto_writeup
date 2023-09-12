from cypari2 import Pari 
from math import floor, gcd
from Crypto.Util.number import inverse
from mpmath import *
mp.dps = 100

pari = Pari()

modulus = [187, 5893, 7171, 3439, 799] 
# fermat's attack : kraitchik approch
def fermat(N):
    a = floor(pari.sqrt(N))
    x = abs(a**2 - N)
    b = 1
    while not pari.issquare(x):
        a += 1
        x = abs(a**2 - N)

    return gcd(a-floor(pari.sqrt(x)), N), gcd(a+floor(pari.sqrt(x)), N)

# test fermat
""" for n in modulus:
    print(n, "\t:\t", fermat(n)) """



# continued fraction of a/b
def continued_frac(a,b):
    if a < b:
        cont_frac = [0]
        a,b = b,a
    else:
        cont_frac = []
    r = a%b
    while r != 0:
        cont_frac.append(a//b)
        a,b = b, r
        r = a%b
    cont_frac.append(a)
    return cont_frac

def frac_from_contfrac(cont_frac):
    reversed = False
    if cont_frac[0] == 0:
        reversed = True
        cont_frac = cont_frac[1:]
    num = cont_frac[-1]
    den = 1
    for x in cont_frac[-2::-1]:
        num, den = num*x + den, num
    if reversed:
        return den, num
    return num, den
        
#print(frac_from_contfrac([2,3,1,1,9,1,1,48]))

def reduced_cont_frac(cont_frac):
    if cont_frac[0] == 0:
        return [cont_frac[:i] for i in range(2, len(cont_frac)+1)]
    return [cont_frac[:i] for i in range(1, len(cont_frac))]

#print(reduced_cont_frac([2,3,1,1,9,1,1,48]))

def factor_from_n_phi(phi_n, N):
    b = N - phi_n + 1
    delta = b**2 - 4*N 
    if delta < 0:
        return 1,1
    p = mpf((b - mpf(sqrt(delta))) / 2)
    q = mpf((b + mpf(sqrt(delta))) / 2)
    
    return p,q

# wiener attack
def wiener(N, e):
    found = False
    p=q=1
    cont_frac = continued_frac(e, N)
    
    for rd in reduced_cont_frac(cont_frac):
        k, d = frac_from_contfrac(rd)
        if (e*d - 1) % k != 0:
            continue
        phi_n = (e*d - 1)//k
        p,q = factor_from_n_phi(phi_n, N)

        if p*q == N:
            found = True
            break 
    if found:
        return p,q
    print("Failed ! maybe the condition is not satisfied (d < (1/3)*N^(1/4))")
    return None,None

#print(wiener(616830313971863461474580904709, 616438096790422722768322924283))
