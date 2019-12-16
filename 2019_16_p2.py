from aoc import read_file, timer

@timer
def solve():
    input    = read_file("16")[0]
    offset   = int(input[:7])
    elements = [int(num) for _ in range(10000) for num in input][offset:]
    
    for _ in range(100):
        for i in range(-2, -len(elements)-1, -1):
            elements[i] = (elements[i] + elements[i+1]) % 10

    return "".join([str(x) for x in elements[:8]])

result = solve()
print(f"Solution: {result}")