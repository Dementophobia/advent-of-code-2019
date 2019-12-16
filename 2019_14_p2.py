from aoc import read_file, timer
from collections import defaultdict

def produce(comp, amount, requirements, rest = None):
    if rest == None:
        rest = defaultdict(int)

    for prod, sources in requirements.items():
        if prod[1] == comp:
            break

    made = rest[prod[1]]

    if not (amount - made) % prod[0]:
        rest[prod[1]] = 0
        a = (amount - made) // prod[0]
    else:
        rest[prod[1]] = prod[0] - ((amount - made) % prod[0])
        a = (amount - made) // prod[0] + 1

    ore = 0
    
    for source in sources:
        if source[1] == "ORE":
             ore += source[0]*a
        else:
            cost = produce(source[1], source[0]*a, requirements, rest)
            ore += cost

    return ore
        
@timer
def solve():
    input = read_file("14")

    req = defaultdict(list)
    
    for line in input:
        line = list(line)
        while "," in line:
            line.remove(",")
        line = "".join(line)
        
        x = line.split(" ")
        comps = (len(x) - 3) // 2
        for i in range(comps):
            req[(int(x[-2]), x[-1])].append((int(x[i*2]), x[i*2+1]))

    available = 1000000000000

    low = available // produce("FUEL", 1, req)
    high = 2 * low
    
    while high - low > 1:
        middle = (high + low) // 2
        cost = produce("FUEL", middle, req)
        if cost <= available:
            low = middle
        else:
            high = middle
    
    return low


result = solve()
print(f"Solution: {result}")