import mpmath as mp
from src.leading_window import *
from src.mantissa_digits import power_digits_integer
from src.gamma_formulas import finite_bias_gamma
from src.discrepancy import ordinary_discrepancy
mp.mp.dps=60
def test_d3_exact_vs_observable():
    for a,b in ((2,10),(3,2),(5,8)):
        alpha=mp.log(a)/mp.log(b)
        for n in range(1,80):
            J=min(5,len(power_digits_integer(a,n,b)))
            assert leading_sum_exact(a,n,b,J)==leading_observable(b,J,(n*alpha)%1)
def test_d4_prefix_enumeration():
    from src.exact_digit_laws import expected_prefix_digit_sum_enumeration
    for b,J in ((2,6),(3,4),(10,3)):
        assert abs(expected_prefix_digit_sum_enumeration(b,J)-(J*mp.mpf(b-1)/2-finite_bias_gamma(b,J)))<mp.mpf('1e-48')
def test_d5_bound():
    for a,b in ((2,10),(3,10),(2,3),(3,2),(5,8)):
        N,J=300,3; alpha=mp.log(a)/mp.log(b)
        D=ordinary_discrepancy([float((n*alpha)%1) for n in range(1,N+1)])
        e=short_count(a,b,N,J); target=J*mp.mpf(b-1)/2-finite_bias_gamma(b,J)
        err=abs(empirical_leading_average(a,b,N,J)-target)
        rhs=mp.mpf(b-1)/2*b**J*D+(b-1)*J*mp.mpf(e)/N
        assert err<=rhs+mp.mpf('1e-40')
