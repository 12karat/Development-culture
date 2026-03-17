import sys
#T000 make with "pip install -e"
sys.path.append("../src")

from math demo import add

def test_addition_basic():
    assert add(2, 2) == 4, "function didn't returned 4"
    print("Test BASIC ADDITION PASSED")

def test_bug_addition_notsufficient():
    assert add(2, 2) == 4, "function didn't returned 4"
    print("Test BUG ADDITION PASSED")

def test_bug_addition_enough():
    assert add_with_bug(2, 2) == 4, "function didn't returned 4"
    assert add_with_bug(0, 0) == 0
    assert add_with_bug(5, 6) == 11
    print("Test BUG ADDITION PASSED")

def test_addicion_duplicated_logic():
    #bad test since input and output are independent from add()
    assert add(6, 3) == 6 + 3
    #done
    assert add(6, 3) == 9
    print("Test DUPLICATED LOGIC PASSED")

def test_addition_overcomplicated():
    for i in range(0, 2**32):
        for j in range(0, 2**32):
            assert add(i, j) == i + j
            assert add(-i, j) == -i + j
            assert add(i, -j) == i - j
            assert add(-i, -j) == -i - j

def test_addition_resonable():
    assert add(6, 3) == 9
    assert add(0, 3) == 3
    assert add(0, -3) == -3
    assert add(-7, 83) == 76
    assert add(-7, -83) == -90
    print("Test ADDITION with RESONABLE NUMBER of CASES PASSED")

def test_add_something_resonable():
    add_something(6, 3) == 9
    add_something(None, None) == 0
    add_something(None, "abc") == 0
    add_something(None, 10) == 0
    add_something("abc", 10) == "abc10"
    add_something(10, "abc") == "10abc"
    add_something("xyz", "abc") == "xyzabc"
    print("Test ANOTHER ADDITION with RESONABLE NUMBER of CASES PASSED")

def test_tax_calculation():
    #using only integers doesnt allow test all cases
    assert calculate_tax(1000) == 150
    assert calculate_tax(2000) == 300
    assert calculate_tax(30) == 4.5
    assert calculate_tax(1) == .15
    
    print("Test TAX CALCULATION PASSED")

if __name__ = "__main__":
    test_addition_basic()  
    test_bug_addition_notsufficient()
    test_bug_addition_enough()
    test_addicion_dublicated_logic()
    test_add_something_resonable()
    test_addition_resonable()
    test_tax_calculation()
    



