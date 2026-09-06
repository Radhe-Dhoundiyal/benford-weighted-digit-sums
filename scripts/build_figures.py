from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path('outputs/tables'); F=Path('outputs/figures'); F.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(T/'bias_convergence.csv')
for b in (2,3,10,16):
 x=d[d.base==b]; plt.semilogy(x.L,abs(x.residual),marker='o',label=f'b={b}')
plt.xlabel('L'); plt.ylabel('|c_b-c_{b,L}|'); plt.legend(); plt.tight_layout(); plt.savefig(F/'bias_convergence.png',dpi=160); plt.close()
d=pd.read_csv(T/'digit_asymptotic_scaled_residuals.csv')
for b in (2,3,10,16):
 x=d[d.base==b].groupby('j').scaled_residual.apply(lambda z:max(abs(z))); plt.plot(x.index,x.values,marker='o',label=f'b={b}')
plt.xlabel('j'); plt.ylabel('max_r |scaled residual|'); plt.legend(); plt.tight_layout(); plt.savefig(F/'deep_digit_scaled_residual.png',dpi=160); plt.close()
d=pd.read_csv(T/'deterministic_residuals_and_bounds.csv'); d.second_order_residual=pd.to_numeric(d.second_order_residual)
for a,b in ((2,10),(3,10),(2,3),(3,2)):
 x=d[(d.a==a)&(d.b==b)]; plt.plot(x.N,x.second_order_residual,marker='o',label=f'({a},{b})')
plt.axhline(0,color='black',lw=.6); plt.xlabel('N'); plt.ylabel('second-order residual'); plt.legend(); plt.tight_layout(); plt.savefig(F/'deterministic_residual.png',dpi=160); plt.close()
print('figures built')
