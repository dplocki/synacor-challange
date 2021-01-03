from itertools import permutations

digits = [2, 7, 9, 3, 5]
permutations = ((a, b, c, d, e) for a, b, c, d, e in permutations(digits, 5) if a + b * c ** 2 + d ** 3 - e == 399)
a, b, c, d, e = next(permutations)
print(f'{a} + {b} * {c}^2 + {d}^3 - {e} = 399')
