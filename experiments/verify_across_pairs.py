from pathlib import Path
import csv, random, mpmath as mp
from src.mantissa_digits import multiplicatively_dependent,power_digits_integer,power_digits_mantissa
from src.discrepancy import ordinary_discrepancy,star_discrepancy
from src.leading_window import empirical_leading_average,short_count
from src.gamma_formulas import finite_bias_gamma
from src.bias_constant import bias_closed
mp.mp.dps=80
OUT=Path('outputs/tables'); OUT.mkdir(parents=True,exist_ok=True)
pairs=[(2,10),(3,10),(7,10),(11,10),(2,3),(3,2),(5,8),(7,16),(11,16),(10,3),(13,7),(17,12),(19,5)]
negative=[(2,4),(2,8),(4,2),(10,10),(3,9)]
dig=[]; det=[]; disc=[]
for a,b in pairs:
    mism=total=0
    for n in range(1,251):
        exact=power_digits_integer(a,n,b); J=min(10,len(exact)); total+=J
        mism += sum(x!=y for x,y in zip(exact[:J],power_digits_mantissa(a,n,b,J,130)))
    dig.append({'a':a,'b':b,'cases':250,'digits_compared':total,'mismatches':mism})
    alpha=mp.log(a)/mp.log(b)
    for N in (200,500,1000):
        J=max(1,int(mp.floor(mp.log(N)/(4*mp.log(b)))))
        pts=[float((n*alpha)%1) for n in range(1,N+1)]
        D=ordinary_discrepancy(pts); Ds=star_discrepancy(pts); e=short_count(a,b,N,J)
        S=empirical_leading_average(a,b,N,J); finite=J*mp.mpf(b-1)/2-finite_bias_gamma(b,J)
        obs=abs(S-finite); rhs=mp.mpf(b-1)/2*b**J*D+(b-1)*J*mp.mpf(e)/N
        residual=S-(J*mp.mpf(b-1)/2-bias_closed(b))
        row={'a':a,'b':b,'N':N,'J':J,'ordinary_D':D,'star_D':Ds,'short_count':e,'observed_error':mp.nstr(obs,18),'bound_rhs':mp.nstr(rhs,18),'bound_holds':obs<=rhs,'second_order_residual':mp.nstr(residual,18),'bJ_D':float(b**J*D),'J2_over_N':float(J*J/N)}
        det.append(row); disc.append({k:row[k] for k in ('a','b','N','ordinary_D','star_D')})
for a,b in negative: dig.append({'a':a,'b':b,'cases':0,'digits_compared':0,'mismatches':'DEPENDENT-DETECTED' if multiplicatively_dependent(a,b) else 'ERROR'})
def write(name,rows):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
write('digit_extraction_mismatches.csv',dig); write('deterministic_residuals_and_bounds.csv',det); write('discrepancy_values.csv',disc)
print('pair rows',len(dig)+len(det)+len(disc))
