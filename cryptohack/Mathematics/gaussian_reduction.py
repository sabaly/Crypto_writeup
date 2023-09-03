from math import floor 

def normVec(v):
    norm = 0
    for x in v:
        norm+=x**2
    return norm 

def vec_prod(v1,v2):
    if len(v1) != len(v2):
        raise 'incorrect vector length'
    result = 0
    for i in range(len(v1)):
        result += v1[i]*v2[i]
    return result

def vec_scal_prod(scal, v):
    return [scal*x for x in v]

def add_vec(v1,v2, type='+'):
    if len(v1) != len(v2):
        raise 'incorrect vector length'
    if type == '+':
        return [v1[i]+v2[i] for i in range(len(v1))]
    else:
        return [v1[i]-v2[i] for i in range(len(v1))]
def GR(v1,v2):
    while True:
        if normVec(v2) < normVec(v1):
            v1,v2 = v2,v1
        m = floor(vec_prod(v1,v2)/normVec(v1))
        if m == 0 :
            return v1,v2
        v2 = add_vec(v2,vec_scal_prod(m,v1),'-')

v = (846835985, 9834798552)
u = (87502093, 123094980)

u,v = GR(u,v)
print(u,v)
print(vec_prod(u,v))

