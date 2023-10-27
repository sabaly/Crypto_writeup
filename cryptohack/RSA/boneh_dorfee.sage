import time
# return || pol ||^2
def norm_pol(Pol): 
    coefs = Pol.coefficients()
    return sum([x**2 for x in coefs])

def get_g_s_poly(f, u, x, y, e, m, X, Y, U, Q):
    g_s = []
    for k in range(m+1):
        for i in range(m-k+1):
            tmp = (x)**i * f(u, x, y)**k * e**(m-k)
            g_s.append(Q(tmp).lift())

    return g_s

def get_h_s_poly(f, u, x, y, e, m, t, X, Y, U, Q):
    h_s = []
    for j in range(1, t+1):
        for k in range(floor(m/t)*j, m+1):
            tmp = (y)**j * f(u, x, y)**k * e**(m-k)
            h_s.append(Q(tmp).lift())
    return h_s

def get_matrix(pols, U,X,Y, monomials, bound):
    n = len(monomials)
    M = Matrix(ZZ, n)
    
    for i in range(n):
        M[i,0] = pols[i].constant_coefficient()
        for j in range(1, i+1):
            if monomials[j] in pols[i].monomials():
                M[i,j] = pols[i].monomial_coefficient(monomials[j])*monomials[j](U,X,Y)

    return M

def get_poly(coefs, monomials, X,Y,U):
    PR.<v,w> = PolynomialRing(ZZ)
    poly = 0
    for i in range(len(monomials)):
        poly += monomials[i](v*w+1, v, w) * coefs[i] / monomials[i](U,X,Y)

    return poly
    
def boneh_dorfee(N, e):
    delta = 0.284
    X = 2*floor(N**delta)
    Y = floor(N**(1/2))
    A = (N+1)/2

    K.<u,x,y> = ZZ[]
    u = K.gens()[0]
    x = K.gens()[1]
    y = K.gens()[2]
    Q = K.quotient(x*y + 1 - u)
    f = Q(x*(A + y) + 1).lift()
    U = X*Y + 1
    stop = False
    m = 5
    bound = e**m
    t = ceil(m*(1-2*delta)/2)
    start_time = time.time()
    xx=yy=-1 # final solution
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
        for j in range(1, t+1):
            for k in range(floor(m/t)*j, m+1):
                monomials.append(u**k * y**j)
        
        M = get_matrix(g_s + h_s, U, X, Y, monomials, bound)
        
        M = M.LLL()
        n = len(monomials)
        
        pols_found = false
        for i in range(n-1):
            g1 = get_poly(M[i], monomials, X,Y,U)
            for k in range(i+1, n):
                g2 = get_poly(M[k], monomials, X,Y,U)
        
                if g1.is_zero() or g2.is_zero():
                    continue
                # resultante
                PR.<q> = PolynomialRing(ZZ)
                r = g1.resultant(g2)
                if r.is_zero() or r.monomials() == [1]:
                    continue
                else:
                    pols_found = True
                    break
            if pols_found:
                break
        if not pols_found:
            m+=1
            t = ceil(m*(1-2*delta)/2)
            bound = e**m
            continue
        
        r = r(q,q)
        #print("r = ", r)
        sols = r.roots()
        if len(sols) == 0:
            break
        yy = sols[0][0]
        print(yy)
        g1 = g1(q,yy)
        sols = g1.roots()
        if len(sols) == 0:
            m+=1
            t = ceil(m*(1-2*delta)/2)
            bound = e**m
        else:
            xx = sols[0][0]
            break
        if time.time() - start_time > 10:
            print("Taking toooo long...")
            break 
    if xx<0:
        print("Wrong polynome x < 0")
        return -1
    else:
        P.<x,y> = PolynomialRing(ZZ)
        A = int((N+1)/2)
        pol = 1 + x * (A + y)
        return int(pol(xx,yy)/e)

def example():
    N = 0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b
    e = 0x9d0637faa46281b533e83cc37e1cf5626bd33f712cc1948622f10ec26f766fb37b9cd6c7a6e4b2c03bce0dd70d5a3a28b6b0c941d8792bc6a870568790ebcd30f40277af59e0fd3141e272c48f8e33592965997c7d93006c27bf3a2b8fb71831dfa939c0ba2c7569dd1b660efc6c8966e674fbe6e051811d92a802c789d895f356ceec9722d5a7b617d21b8aa42dd6a45de721953939a5a81b8dffc9490acd4f60b0c0475883ff7e2ab50b39b2deeedaefefffc52ae2e03f72756d9b4f7b6bd85b1a6764b31312bc375a2298b78b0263d492205d2a5aa7a227abaf41ab4ea8ce0e75728a5177fe90ace36fdc5dba53317bbf90e60a6f2311bb333bf55ba3245f

    d = boneh_dorfee(N, e)
    if d == -1:
        print("Didn't work !")
    else:
        print("Private key found d = ", d)
# example()
# source : 
# https://www.davidwong.fr/papers/david_wong_rsa_lll_boneh_durfee__2015.pdf
#
