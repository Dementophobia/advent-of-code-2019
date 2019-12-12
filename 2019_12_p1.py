from aoc import read_file, timer
from re import findall

def extract_ints(line):
    return [int(x) for x in findall(r'-?\d+', line)]

def apply_gravity(moons, velocities):
    for m_1 in range(3):
        for m_2 in range(m_1+1, 4):
            for dim in range(3):
                if moons[m_1][dim] > moons[m_2][dim]:
                    velocities[m_1][dim] -= 1
                    velocities[m_2][dim] += 1
                elif moons[m_1][dim] < moons[m_2][dim]:
                    velocities[m_1][dim] += 1
                    velocities[m_2][dim] -= 1

def apply_velocity(moons, velocities):
    for m in range(4):
        for dim in range(3):
            moons[m][dim] += velocities[m][dim]

def calculate_energy(moons, velocities):
    e = 0
    for i in range(4):
        pot = sum([abs(moon) for moon in moons[i]])
        kin = sum([abs(velocity) for velocity in velocities[i]])
        e += pot * kin
    return e

@timer
def solve():
    input = read_file("12")

    moons       = [extract_ints(line) for line in input]
    velocities  = [[0 for x in range(3)] for y in range(4)]

    for _ in range(1000):
        apply_gravity(moons, velocities)
        apply_velocity(moons, velocities)

    return calculate_energy(moons, velocities)

result = solve()
print(f"Solution: {result}")