from cypari2 import Pari 
from math import floor, gcd
from Crypto.Util.number import inverse
from mpmath import *
from random import randint
from sage.all import *
from decimal import Decimal

mp.dps = 100


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
"""
modulus = [187, 5893, 7171, 3439, 799]  
for n in modulus:
    print(n, "\t:\t", fermat(n)) """


""" 
This section we implement wiener attack base on continued fractions.
"""
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

# reconstiture fraction from it's continued form
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

# wiener attack for factoring N
def wiener_factor(N, e):
    found = False
    p=q=1
    cont_frac = continued_frac(e, N)
    
    for rd in reduced_cont_frac(cont_frac):
        k, d = frac_from_contfrac(rd)
        if (e*d - 1) % k != 0 and k == d:
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

# finding a small d with wiener attack
def wiener(N, e):
    pari = Pari()
    cont_frac = continued_frac(e, N)
    for rd in reduced_cont_frac(cont_frac):
        if (len(rd)-1)%2==0:
            rd[-1] += 1 
            k, dg = frac_from_contfrac(rd)
        else:
            k, dg = frac_from_contfrac(rd)
        g = e*dg % k
        if g == 0: # means this k and dg  are wrong guests
            continue
        phi = e*dg // k
        
        if (N - phi + 1) % 2 != 0:  # means x is not an integer
            continue
        x = (N - phi + 1)//2 # represent (p+q)/2
        y = x**2 - N # represente ((p-q)/2)^2
        if pari.issquare(y):
            d = dg//g
            if d!=1:
                return d

    print('oups ! wiener attack did not work')
    return -1

# The following 
def factor_N_from_d(N,e,d):
    k = e*d - 1
    g = randint(2, N-1)
    round = 0
    while k%2 == 0:
        k//=2
        x = pow(g, k, N)
        p=gcd(x-1,N)
        if x > 1 and p > 1:
            return p
        
        if k%2 == 1:
            k = e*d - 1
            g = randint(2, N-1)
            round+=1
            if round > 40:
                break
    return -1
