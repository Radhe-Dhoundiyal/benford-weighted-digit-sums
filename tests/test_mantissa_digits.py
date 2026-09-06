from src.mantissa_digits import *
def test_dependency_exact():
    for p in ((2,4),(2,8),(4,2),(10,10),(3,9)): assert multiplicatively_dependent(*p)
    for p in ((2,10),(3,10),(7,10),(2,3),(3,2),(5,8),(7,16)): assert not multiplicatively_dependent(*p)
def test_two_digit_paths():
    for a,b in ((2,10),(3,10),(7,10),(2,3),(3,2),(5,8),(7,16),(11,16),(10,3)):
        for n in range(1,101):
            exact=power_digits_integer(a,n,b); J=min(8,len(exact))
            assert exact[:J]==power_digits_mantissa(a,n,b,J,120)
