from pathlib import Path
import csv, mpmath as mp
from src.bias_constant import bias_closed,tail_expansion,tail_bound
from src.gamma_formulas import finite_bias_gamma,expected_digit_gamma_closed
from src.exact_digit_laws import expected_digit_raw,raw_digit_probability
from src.asymptotics import digit_scaled_residual
mp.mp.dps=220
OUT=Path('outputs/tables'); OUT.mkdir(parents=True,exist_ok=True)
bases=(2,3,4,5,6,7,8,9,10,12,16,20,32)
def write(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
cb=[]; conv=[]; ex=[]; asym=[]; tails=[]
for b in bases:
    c=bias_closed(b); cb.append({'base':b,'c_b':mp.nstr(c,50)})
    for L in range(1,13):
        cl=finite_bias_gamma(b,L); conv.append({'base':b,'L':L,'c_b_L':mp.nstr(cl,40),'residual':mp.nstr(c-cl,15)})
        eps=c-cl-tail_expansion(b,L); bound=tail_bound(b,L)
        tails.append({'base':b,'L':L,'epsilon':mp.nstr(eps,15),'bound':mp.nstr(bound,15),'ratio':mp.nstr(abs(eps)/bound,15)})
    for j in range(2, min(7,4 if b>=10 else 6)):
        raw=expected_digit_raw(b,j); gam=expected_digit_gamma_closed(b,j)
        ex.append({'base':b,'j':j,'raw':mp.nstr(raw,35),'gamma':mp.nstr(gam,35),'residual':mp.nstr(abs(raw-gam),10)})
        for r in range(b): asym.append({'base':b,'j':j,'r':r,'scaled_residual':mp.nstr(digit_scaled_residual(raw_digit_probability(b,j,r),b,j,r),20)})
write('bias_constants.csv',cb); write('bias_convergence.csv',conv); write('expectation_residuals.csv',ex)
write('digit_asymptotic_scaled_residuals.csv',asym); write('tail_bound_ratios.csv',tails)
print('across-bases rows',len(cb)+len(conv)+len(ex)+len(asym)+len(tails))
