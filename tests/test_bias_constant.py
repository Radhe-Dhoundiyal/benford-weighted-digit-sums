import mpmath as mp
from src.bias_constant import *
from src.gamma_formulas import finite_bias_gamma
mp.mp.dps=80
def test_a5_three_methods():
    for b in (2,3,5,10,16):
        for L in range(1, 6 if b <= 3 else 4):
            vals=[finite_bias_direct(b,L),finite_bias_gamma(b,L),finite_bias_factorial(b,L)]
            assert max(vals)-min(vals)<mp.mpf('1e-60')
def test_a7_convergence():
    for b in (2,3,4,5,6,7,8,9,10,12,16,20,32): assert abs(finite_bias_gamma(b,15)-bias_closed(b))<mp.mpf(b)**(-14)
