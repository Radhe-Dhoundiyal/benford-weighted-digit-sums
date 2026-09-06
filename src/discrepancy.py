"""Exact one-dimensional empirical star and ordinary interval discrepancy."""
def star_discrepancy(points):
    xs=sorted(float(x)%1.0 for x in points); n=len(xs)
    if not n: raise ValueError
    return max(max((i+1)/n-x for i,x in enumerate(xs)),
               max(x-i/n for i,x in enumerate(xs)))

def ordinary_discrepancy(points):
    xs=sorted(float(x)%1.0 for x in points); n=len(xs)
    if not n: raise ValueError
    # range of F_N(t)-t over both one-sided values at each jump
    vals=[0.0]
    for i,x in enumerate(xs): vals.extend((i/n-x,(i+1)/n-x))
    vals.append(0.0)
    return max(vals)-min(vals)

def brute_ordinary_discrepancy(points):
    import math
    xs=sorted(float(x)%1.0 for x in points)
    endpoints=sorted(set([0.0,1.0,*xs,*(math.nextafter(x,1.0) for x in xs)])); n=len(xs)
    best=0.0
    for u in endpoints:
        for v in endpoints:
            if u<=v:
                count=sum(u<=x<v for x in xs)
                best=max(best,abs(count/n-(v-u)))
    return best
