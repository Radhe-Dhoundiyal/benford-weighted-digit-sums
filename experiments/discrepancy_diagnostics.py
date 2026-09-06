from src.discrepancy import ordinary_discrepancy,star_discrepancy,brute_ordinary_discrepancy
for xs in ([.2],[.1,.7],[.05,.25,.51,.92]): print(xs,star_discrepancy(xs),ordinary_discrepancy(xs),brute_ordinary_discrepancy(xs))
