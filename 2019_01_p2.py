from aoc import read_file, timer

def calc_cost(mass):
    return mass // 3 - 2

@timer
def solve():
    input = read_file("01")
    mass = [int(x) for x in input]
    
    result = 0
    
    for m in mass:
        while (m := calc_cost(m)) > 0:
            result += m
    
    return result

result = solve()
print(f"Solution: {result}")