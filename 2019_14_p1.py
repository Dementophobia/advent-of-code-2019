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
    requirements = defaultdict(list)

    for line in input:
        parts = line.replace(",", "").split(" ")
        for i in range((len(parts) - 3) // 2):
            requirements[(int(parts[-2]), parts[-1])].append((int(parts[i*2]), parts[i*2+1]))

    return produce("FUEL", 1, requirements)

result = solve()
print(f"Solution: {result}")