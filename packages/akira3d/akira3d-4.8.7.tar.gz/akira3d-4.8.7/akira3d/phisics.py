import time

def vecLen(v): return (v[0]**2+v[1]**2+v[2]**2)**0.5

def normVec(v):
    nl = vecLen(v)
    if nl != 0:
        nl = 1/nl
        return [v[0]*nl, v[1]*nl, v[2]*nl]
    else:
        return [0, 0, 0]

class F:
    def __init__(self, v, m):
        self.v = v
        self.m = m
        self.f = [i*m for i in v]
    
    def sum(self, f, c=1):
        f1 = [self.f[i] + f.f[i]*c for i in range(3)]
        if f1 !=[0, 0, 0]:
            m = vecLen(f1)
            v = normVec(f1)
            return F(v, m)
        else:
            return F([0, 0, 0], 0)
    
    def mul(self, f):
        f1 = [self.f[i]*f.f[i] for i in range(3)]
        if f1 !=[0, 0, 0]:
            m = vecLen(f1)
            v = normVec(f1)
            return F(v, m)
        else:
            return F([0, 0, 0], 0)
    
    def roundVec(self): 
        self.f = [round(i, 3) for i in self.f]
        if self.f != [0, 0, 0]:
            m = vecLen(self.f)
            v = normVec(self.f)
            return F(v, m)
        else:
            return F([0, 0, 0], 0)


def mul(f1, f2):
    f = [f1.f[i]*f2.f[i] for i in range(3)]
    if f !=[0, 0, 0]:
        m = vecLen(f1)
        v = normVec(f1)
        return F(v, m)
    else:
        return F([0, 0, 0], 0)
