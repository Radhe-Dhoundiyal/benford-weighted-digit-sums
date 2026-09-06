"""Gamma formulas kept independent of raw prefix summation."""
import mpmath as mp

def gamma_digit_probability(b,j,r):
    if b < 2 or j < 2 or r not in range(b): raise ValueError
    M=mp.mpf(b)**(j-2)
    z=(mp.loggamma(b*M+mp.mpf(r+1)/b)+mp.loggamma(M+mp.mpf(r)/b)
       -mp.loggamma(b*M+mp.mpf(r)/b)-mp.loggamma(M+mp.mpf(r+1)/b))
    return z/mp.log(b)

def expected_digit_gamma_probability(b,j):
    return mp.fsum(r*gamma_digit_probability(b,j,r) for r in range(b))

def expected_digit_gamma_closed(b,j):
    if j < 2: raise ValueError
    M=mp.mpf(b)**(j-2)
    return ((b-1)*(1+b*M)+((b+1)*mp.loggamma(b*M)-b*mp.loggamma(M)
            -mp.loggamma(b*b*M))/mp.log(b))

def finite_bias_gamma(b,L):
    B=mp.mpf(b)**L
    return ((mp.loggamma(B)-b*mp.loggamma(B/b))/mp.log(b)
            -(B-b)-mp.mpf(L)*(b-1)/2)

def expected_prefix_digit_sum_factorial(b,L):
    B=mp.mpf(b)**L; A=B/b
    return (B-b+L*(b-1)-(mp.loggamma(B)-b*mp.loggamma(A))/mp.log(b))
