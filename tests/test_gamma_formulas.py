import mpmath as mp
from src.exact_digit_laws import raw_digit_probability,expected_digit_raw
from src.gamma_formulas import *
mp.mp.dps=70
def test_a2():
    for b in (2,3,5,10,16):
        for j in range(2, 7 if b <= 3 else 5):
            for r in range(b): assert abs(raw_digit_probability(b,j,r)-gamma_digit_probability(b,j,r))<mp.mpf('1e-55')
def test_a4_three_paths():
    for b in (2,3,10,16):
        for j in range(2, 7 if b <= 3 else 5):
            a=expected_digit_raw(b,j); g=expected_digit_gamma_probability(b,j); c=expected_digit_gamma_closed(b,j)
            assert max(abs(a-g),abs(a-c))<mp.mpf('1e-50')
