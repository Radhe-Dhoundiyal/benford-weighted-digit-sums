import mpmath as mp
from src.bias_constant import bias_closed
from src.gamma_formulas import finite_bias_gamma
mp.mp.dps=80
for L in range(1,16): print(L,mp.nstr(finite_bias_gamma(10,L),30),mp.nstr(bias_closed(10)-finite_bias_gamma(10,L),8))
