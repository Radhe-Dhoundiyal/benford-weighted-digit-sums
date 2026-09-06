import mpmath as mp
from .exact_digit_laws import expected_digit_raw

def bias_closed(b):
    return mp.mpf(b)/2-mp.mpf(b-1)/2*(mp.log(2*mp.pi)/mp.log(b))

def finite_bias_direct(b,L):
    mu=mp.mpf(b-1)/2
    return mp.fsum(mu-expected_digit_raw(b,j) for j in range(1,L+1))

def finite_bias_factorial(b,L):
    """Independent via E[s_b(M_L)] factorial identity."""
    B=mp.mpf(b)**L; A=B/b
    es=B-b+L*(b-1)-(mp.loggamma(B)-b*mp.loggamma(A))/mp.log(b)
    return L*mp.mpf(b-1)/2-es

def tail_expansion(b,L):
    x=mp.mpf(b)**(-L)
    return ((b*b-1)/(12*mp.log(b))*x
            -(b**4-1)/(360*mp.log(b))*x**3)

def tail_bound(b,L):
    return (b**6+1)/(1260*mp.log(b))*mp.mpf(b)**(-5*L)
