import mpmath as mp
from src.exact_digit_laws import *
mp.mp.dps=60
def test_a1_normalization_and_geometry():
    for b in (2,3,4,5,8,10,16):
        for j in range(2, 5 if b <= 5 else 4):
            ps=[raw_digit_probability(b,j,r) for r in range(b)]
            assert abs(mp.fsum(ps)-1)<mp.mpf('1e-50')
            assert max(abs(ps[r]-interval_digit_probability(b,j,r)) for r in range(b))<mp.mpf('1e-50')
def test_a3():
    for b in range(2,20): assert abs(expected_first_digit(b)-((b-1)-mp.loggamma(b)/mp.log(b)))<mp.mpf('1e-50')
def test_a6_enumeration():
    from src.gamma_formulas import expected_prefix_digit_sum_factorial
    for b,L in ((2,8),(3,5),(5,3),(10,3)):
        assert abs(expected_prefix_digit_sum_enumeration(b,L)-expected_prefix_digit_sum_factorial(b,L))<mp.mpf('1e-48')
