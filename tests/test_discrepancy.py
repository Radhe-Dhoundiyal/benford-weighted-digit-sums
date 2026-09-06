import random
from src.discrepancy import *
def test_ordinary_against_brute():
    rng=random.Random(20260905)
    for n in range(1,12):
        for _ in range(20):
            xs=[rng.random() for _ in range(n)]
            assert abs(ordinary_discrepancy(xs)-brute_ordinary_discrepancy(xs))<1e-14
            assert star_discrepancy(xs)<=ordinary_discrepancy(xs)+1e-14
