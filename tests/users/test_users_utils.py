import pytest
from flaskapp.users.utils import solve, MinCostMatching

def test_MinCostMatching():
    cost = [[-1, -2, -3], [-3, -2, -1], [-3, -1, -2]]
    Lmate = [-1] * 3
    Rmate = [-1] * 3
    result = MinCostMatching(cost, Lmate, Rmate)
    assert result == [(0, 2), (1, 1), (2, 0)]

def test_solve():
    n = 3
    cost = [[-1, -2, -3], [-3, -2, -1], [-3, -1, -2]]
    rent = 6
    result = solve(n, cost, rent)
    assert result == [[2, 2.33], [1, 1.33], [0, 2.33]]
