from aoc import read_file, timer

def calc_cost(mass):
    return mass // 3 - 2

@timer
def solve():
    input = read_file("01")
    mass = [int(x) for x in input]
    return sum([calc_cost(m) for m in mass])

result = solve()
print(f"Solution: {result}")