import mpmath as mp
from src.bias_constant import bias_closed,tail_expansion,tail_bound
from src.gamma_formulas import finite_bias_gamma
mp.mp.dps=100
def test_a10_explicit_bound_stress():
    for b in range(2,34):
        for L in range(1,9):
            eps=bias_closed(b)-finite_bias_gamma(b,L)-tail_expansion(b,L)
            assert abs(eps)<=tail_bound(b,L)
