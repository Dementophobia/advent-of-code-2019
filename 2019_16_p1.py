from aoc import read_file, timer
from collections import deque

@timer
def solve():
    input = read_file("16")[0]
    elements = [int(num) for num in input]

    for phase in range(100):
        for pos in range(len(elements)):
            pattern = deque([p for p in [0, 1, 0, -1] for _ in range(pos+1)])
            pattern.rotate(-1)

            res = 0
            for i in range(len(elements)):
                res += elements[i] * pattern[0]
                pattern.rotate(-1)
            elements[pos] = abs(res) % 10

    return "".join(str(x) for x in elements[:8])

result = solve()
print(f"Solution: {result}")

