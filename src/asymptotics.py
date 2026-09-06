import mpmath as mp

def digit_coefficient(b,r):
    return mp.mpf((b-1)*(b-1-2*r))/(2*b*mp.log(b))

def expectation_coefficient(b):
    return -mp.mpf((b-1)**2*(b+1))/(12*mp.log(b))

def digit_scaled_residual(prob,b,j,r):
    return (prob-mp.mpf(1)/b-digit_coefficient(b,r)*mp.mpf(b)**(-j))*mp.mpf(b)**(2*j)

def expectation_scaled_residual(expectation,b,j):
    return (expectation-mp.mpf(b-1)/2-expectation_coefficient(b)*mp.mpf(b)**(-j))*mp.mpf(b)**(2*j)
