"""Independent exact/logarithmic digit-law implementations."""
import mpmath as mp

def validate_base_position(b, j):
    if not isinstance(b, int) or b < 2 or not isinstance(j, int) or j < 1:
        raise ValueError("require integer b>=2 and j>=1")

def first_digit_probability(b, d):
    validate_base_position(b, 1)
    if d not in range(1, b): raise ValueError("invalid first digit")
    return mp.log(mp.mpf(d + 1) / d) / mp.log(b)

def raw_digit_probability(b, j, r):
    validate_base_position(b, j)
    if j < 2 or r not in range(b): raise ValueError("require j>=2 and 0<=r<b")
    M = b ** (j - 2)
    return mp.fsum(mp.log(mp.mpf(b*q+r+1)/(b*q+r))/mp.log(b)
                   for q in range(M, b*M))

def interval_digit_probability(b, j, r):
    """Geometry path: lengths of theta intervals, not raw_digit_probability."""
    validate_base_position(b, j)
    if j == 1:
        return first_digit_probability(b, r)
    if r not in range(b): raise ValueError("invalid digit")
    lo, hi = b**(j-1), b**j
    total = mp.mpf("0")
    for prefix in range(lo + r, hi, b):
        left = mp.log(mp.mpf(prefix) / lo) / mp.log(b)
        right = mp.log(mp.mpf(prefix + 1) / lo) / mp.log(b)
        total += right-left
    return total

def expected_first_digit(b):
    return mp.fsum(d*first_digit_probability(b,d) for d in range(1,b))

def expected_digit_raw(b,j):
    if j == 1: return expected_first_digit(b)
    return mp.fsum(r*raw_digit_probability(b,j,r) for r in range(b))

def prefix_distribution_probability(b,L,m):
    if not (b**(L-1) <= m < b**L): raise ValueError("invalid prefix")
    return mp.log(mp.mpf(m+1)/m)/mp.log(b)

def digit_sum(n,b):
    s=0
    while n: n,r=divmod(n,b); s+=r
    return s

def expected_prefix_digit_sum_enumeration(b,L):
    return mp.fsum(digit_sum(m,b)*prefix_distribution_probability(b,L,m)
                   for m in range(b**(L-1),b**L))
