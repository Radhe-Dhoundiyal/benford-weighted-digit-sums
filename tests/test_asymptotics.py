import mpmath as mp
from src.exact_digit_laws import raw_digit_probability,expected_digit_raw
from src.asymptotics import *
mp.mp.dps=80
def test_a8_scaled_residual_bounded():
    for b in (2,3,5,10,16):
        for r in range(b): assert max(abs(digit_scaled_residual(raw_digit_probability(b,j,r),b,j,r)) for j in range(3, 9 if b <= 3 else 5))<100*b*b
def test_a9_coefficient_sum_and_numeric():
    for b in (2,3,10,16):
        assert abs(sum(r*digit_coefficient(b,r) for r in range(b))-expectation_coefficient(b))<mp.mpf('1e-70')
        j=8 if b<=3 else 4
        assert abs(expectation_scaled_residual(expected_digit_raw(b,j),b,j))<100*b*b
