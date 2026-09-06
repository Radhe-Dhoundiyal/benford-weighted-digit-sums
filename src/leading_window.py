import math
import mpmath as mp
from .exact_digit_laws import digit_sum
from .mantissa_digits import power_digits_integer

def leading_observable(b,J,theta):
    y=mp.power(b,J-1+theta); nearest=mp.nint(y)
    if abs(y-nearest)<mp.sqrt(mp.eps): y=nearest
    return digit_sum(int(mp.floor(y)),b)

def leading_sum_exact(a,n,b,J):
    digs=power_digits_integer(a,n,b)
    if len(digs)<J: return None
    return sum(digs[:J])

def short_count(a,b,N,J):
    return sum(len(power_digits_integer(a,n,b))<J for n in range(1,N+1))

def empirical_leading_average(a,b,N,J):
    vals=[leading_sum_exact(a,n,b,J) for n in range(1,N+1)]
    return mp.mpf(sum(v for v in vals if v is not None))/N

def digit_intervals(b,j,r):
    if j==1:
        return [(math.log(d,b),math.log(d+1,b)) for d in [r]]
    M=b**(j-2)
    return [(math.log((b*q+r)/(b*M),b),math.log((b*q+r+1)/(b*M),b))
            for q in range(M,b*M)]
