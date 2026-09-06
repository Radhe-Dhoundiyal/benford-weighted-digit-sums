import mpmath as mp
from src.exact_digit_laws import raw_digit_probability
from src.asymptotics import digit_scaled_residual
mp.mp.dps=80
for b in (2,3,10,16):
    for j in range(3, 9 if b<=3 else 5): print(b,j,max(abs(digit_scaled_residual(raw_digit_probability(b,j,r),b,j,r)) for r in range(b)))
