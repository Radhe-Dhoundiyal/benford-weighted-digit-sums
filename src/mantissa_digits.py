"""Exact integer and high-precision mantissa significant digits."""
import math
import mpmath as mp

def integer_to_base(n,b):
    if n < 1 or b < 2: raise ValueError
    out=[]
    while n: n,r=divmod(n,b); out.append(r)
    return out[::-1]

def power_digits_integer(a,n,b):
    return integer_to_base(pow(a,n),b)

def power_digits_mantissa(a,n,b,J,dps=100):
    with mp.workdps(dps):
        x=mp.mpf(n)*mp.log(a)/mp.log(b)
        theta=x-mp.floor(x)
        # tiny downward guard: floor(b^(J-1+theta)) is exact off boundaries;
        # dependent pairs are validated via integers, not this numeric path.
        y=mp.power(b,J-1+theta)
        nearest=mp.nint(y)
        if abs(y-nearest) < mp.power(10,-dps//2): y=nearest
        prefix=int(mp.floor(y))
        digs=integer_to_base(prefix,b)
        if len(digs)<J: digs += [0]*(J-len(digs))
        return digs[:J]

def multiplicatively_dependent(a,b):
    """Exact prime-exponent-vector proportionality test."""
    if a < 2 or b < 2: raise ValueError
    def factor(n):
        f={}; p=2
        while p*p<=n:
            while n%p==0: f[p]=f.get(p,0)+1; n//=p
            p += 1 if p==2 else 2
        if n>1: f[n]=f.get(n,0)+1
        return f
    fa,fb=factor(a),factor(b)
    if set(fa)!=set(fb): return False
    p=next(iter(fa)); return all(fa[q]*fb[p]==fb[q]*fa[p] for q in fa)

def digit_length_power(a,n,b):
    return len(power_digits_integer(a,n,b))
