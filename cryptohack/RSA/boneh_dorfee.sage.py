

# This file was *autogenerated* from the file boneh_dorfee.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_4 = Integer(4); _sage_const_0 = Integer(0); _sage_const_0p284 = RealNumber('0.284'); _sage_const_5 = Integer(5); _sage_const_10 = Integer(10); _sage_const_0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b = Integer(0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b); _sage_const_0x9d0637faa46281b533e83cc37e1cf5626bd33f712cc1948622f10ec26f766fb37b9cd6c7a6e4b2c03bce0dd70d5a3a28b6b0c941d8792bc6a870568790ebcd30f40277af59e0fd3141e272c48f8e33592965997c7d93006c27bf3a2b8fb71831dfa939c0ba2c7569dd1b660efc6c8966e674fbe6e051811d92a802c789d895f356ceec9722d5a7b617d21b8aa42dd6a45de721953939a5a81b8dffc9490acd4f60b0c0475883ff7e2ab50b39b2deeedaefefffc52ae2e03f72756d9b4f7b6bd85b1a6764b31312bc375a2298b78b0263d492205d2a5aa7a227abaf41ab4ea8ce0e75728a5177fe90ace36fdc5dba53317bbf90e60a6f2311bb333bf55ba3245f = Integer(0x9d0637faa46281b533e83cc37e1cf5626bd33f712cc1948622f10ec26f766fb37b9cd6c7a6e4b2c03bce0dd70d5a3a28b6b0c941d8792bc6a870568790ebcd30f40277af59e0fd3141e272c48f8e33592965997c7d93006c27bf3a2b8fb71831dfa939c0ba2c7569dd1b660efc6c8966e674fbe6e051811d92a802c789d895f356ceec9722d5a7b617d21b8aa42dd6a45de721953939a5a81b8dffc9490acd4f60b0c0475883ff7e2ab50b39b2deeedaefefffc52ae2e03f72756d9b4f7b6bd85b1a6764b31312bc375a2298b78b0263d492205d2a5aa7a227abaf41ab4ea8ce0e75728a5177fe90ace36fdc5dba53317bbf90e60a6f2311bb333bf55ba3245f)
import time

def factor_from_n_phi(phi_n, N):
    b = N - phi_n + _sage_const_1 
    delta = b**_sage_const_2  - _sage_const_4 *N 
    if delta < _sage_const_0 :
        return _sage_const_1 ,_sage_const_1 
    p = (b - sqrt(delta)) / _sage_const_2 
    q = (b + sqrt(delta)) / _sage_const_2 
    return p,q

# return || pol ||^2
def norm_pol(Pol): 
    coefs = Pol.coefficients()
    return sum([x**_sage_const_2  for x in coefs])

def get_g_s_poly(f, u, x, y, e, m, X, Y, U, Q):
    g_s = []
    for k in range(m+_sage_const_1 ):
        for i in range(m-k+_sage_const_1 ):
            tmp = (x)**i * f(u, x, y)**k * e**(m-k)
            g_s.append(Q(tmp).lift())

    return g_s

def get_h_s_poly(f, u, x, y, e, m, t, X, Y, U, Q):
    h_s = []
    for j in range(_sage_const_1 , t+_sage_const_1 ):
        for k in range(floor(m/t)*j, m+_sage_const_1 ):
            tmp = (y)**j * f(u, x, y)**k * e**(m-k)
            h_s.append(Q(tmp).lift())
    return h_s

def get_matrix(pols, U,X,Y, monomials, bound):
    n = len(monomials)
    M = Matrix(ZZ, n)
    
    for i in range(n):
        M[i,_sage_const_0 ] = pols[i].constant_coefficient()
        for j in range(_sage_const_1 , i+_sage_const_1 ):
            if monomials[j] in pols[i].monomials():
                M[i,j] = pols[i].monomial_coefficient(monomials[j])*monomials[j](U,X,Y)

    return M

def get_poly(coefs, monomials, X,Y,U):
    PR = PolynomialRing(ZZ, names=('v', 'w',)); (v, w,) = PR._first_ngens(2)
    poly = _sage_const_0 
    for i in range(len(monomials)):
        poly += monomials[i](v*w+_sage_const_1 , v, w) * coefs[i] / monomials[i](U,X,Y)

    return poly
    
def boneh_dorfee(N, e):
    delta = _sage_const_0p284 
    X = _sage_const_2 *floor(N**delta)
    Y = floor(N**(_sage_const_1 /_sage_const_2 ))
    A = (N+_sage_const_1 )/_sage_const_2 

    K = ZZ['u, x, y']; (u, x, y,) = K._first_ngens(3)
    u = K.gens()[_sage_const_0 ]
    x = K.gens()[_sage_const_1 ]
    y = K.gens()[_sage_const_2 ]
    Q = K.quotient(x*y + _sage_const_1  - u)
    f = Q(x*(A + y) + _sage_const_1 ).lift()
    U = X*Y + _sage_const_1 
    stop = False
    m = _sage_const_5 
    bound = e**m
    t = ceil(m*(_sage_const_1 -_sage_const_2 *delta)/_sage_const_2 )
    start_time = time.time()
    xx=yy=-_sage_const_1  # final solution
    while not stop:
        # getting x-shift
        g_s = get_g_s_poly(f, u, x, y, e, m, X, Y, U, Q)
        g_s.sort()
        # getting y-shifts
        h_s = get_h_s_poly(f, u, x, y, e, m, t, X, Y, U, Q)
        
        monomials = []
        for g in g_s:
            for mon in g.monomials():
                if mon not in monomials:
                    monomials.append(mon)
        monomials.sort()
        for j in range(_sage_const_1 , t+_sage_const_1 ):
            for k in range(floor(m/t)*j, m+_sage_const_1 ):
                monomials.append(u**k * y**j)
        
        M = get_matrix(g_s + h_s, U, X, Y, monomials, bound)
        
        M = M.LLL()
        n = len(monomials)
        
        pols_found = false
        for i in range(n-_sage_const_1 ):
            g1 = get_poly(M[i], monomials, X,Y,U)
            for k in range(i+_sage_const_1 , n):
                g2 = get_poly(M[k], monomials, X,Y,U)
        
                if g1.is_zero() or g2.is_zero():
                    continue
                # resultante
                PR = PolynomialRing(ZZ, names=('q',)); (q,) = PR._first_ngens(1)
                r = g1.resultant(g2)
                if r.is_zero() or r.monomials() == [_sage_const_1 ]:
                    continue
                else:
                    pols_found = True
                    break
            if pols_found:
                break
        if not pols_found:
            m+=_sage_const_1 
            t = ceil(m*(_sage_const_1 -_sage_const_2 *delta)/_sage_const_2 )
            bound = e**m
            continue
        
        r = r(q,q)
        #print("r = ", r)
        sols = r.roots()
        if len(sols) == _sage_const_0 :
            break
        yy = sols[_sage_const_0 ][_sage_const_0 ]
        print(yy)
        g1 = g1(q,yy)
        sols = g1.roots()
        if len(sols) == _sage_const_0 :
            m+=_sage_const_1 
            t = ceil(m*(_sage_const_1 -_sage_const_2 *delta)/_sage_const_2 )
            bound = e**m
        else:
            xx = sols[_sage_const_0 ][_sage_const_0 ]
            break
        if time.time() - start_time > _sage_const_10 :
            print("Taking toooo long...")
            break 
    if xx<_sage_const_0 :
        print("Wrong polynome x < 0")
        return -_sage_const_1 
    else:
        P = PolynomialRing(ZZ, names=('x', 'y',)); (x, y,) = P._first_ngens(2)
        A = int((N+_sage_const_1 )/_sage_const_2 )
        pol = _sage_const_1  + x * (A + y)
        return int(pol(xx,yy)/e)


def example():
    N = _sage_const_0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b 
    e = _sage_const_0x9d0637faa46281b533e83cc37e1cf5626bd33f712cc1948622f10ec26f766fb37b9cd6c7a6e4b2c03bce0dd70d5a3a28b6b0c941d8792bc6a870568790ebcd30f40277af59e0fd3141e272c48f8e33592965997c7d93006c27bf3a2b8fb71831dfa939c0ba2c7569dd1b660efc6c8966e674fbe6e051811d92a802c789d895f356ceec9722d5a7b617d21b8aa42dd6a45de721953939a5a81b8dffc9490acd4f60b0c0475883ff7e2ab50b39b2deeedaefefffc52ae2e03f72756d9b4f7b6bd85b1a6764b31312bc375a2298b78b0263d492205d2a5aa7a227abaf41ab4ea8ce0e75728a5177fe90ace36fdc5dba53317bbf90e60a6f2311bb333bf55ba3245f 

    d = boneh_dorfee(N, e)
    if d == -_sage_const_1 :
        print("Didn't work !")
    else:
        print("Private key found d = ", d)
# example()
# source : 
# https://www.davidwong.fr/papers/david_wong_rsa_lll_boneh_durfee__2015.pdf
#

