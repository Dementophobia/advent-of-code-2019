from aoc import read_file, timer
from re import findall

def extract_ints(line):
    return [int(x) for x in findall(r'-?\d+', line)]

def get_prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def calculate_lcm(steps):
    primes_per_dimension = [get_prime_factors(step) for step in steps]
    all_primes = set([prime for primes in primes_per_dimension for prime in primes])
    
    lcm = 1    
    for prime in all_primes:
        amount = max(primes_per_dimension[dim].count(prime) for dim in range(3))
        lcm *= prime**amount
    return lcm

def apply_gravity(moons_dim, velocities_dim):
    for m_1 in range(3):
        for m_2 in range(m_1+1, 4):
            if moons_dim[m_1] > moons_dim[m_2]:
                velocities_dim[m_1] -= 1
                velocities_dim[m_2] += 1
            elif moons_dim[m_1] < moons_dim[m_2]:
                velocities_dim[m_1] += 1
                velocities_dim[m_2] -= 1

def apply_velocity(moons_dim, velocities_dim):
    for m in range(4):
        moons_dim[m] += velocities_dim[m]

def matches_start_state(moons, velocities, moons_dim, velocities_dim, dim):
    for i in range(4):
        if moons[i][dim] != moons_dim[i] or \
           velocities[i][dim] != velocities_dim[i]:
            return False
    return True

@timer
def solve():
    input = read_file("12")

    moons = [extract_ints(line) for line in input]
    velocities = [[0 for x in range(3)] for y in range(4)]

    steps = [0, 0, 0]
   
    for dim in range(3):
        moons_dim = [moon[dim] for moon in moons]
        velocities_dim = [velocity[dim] for velocity in velocities]
        
        while True:
            apply_gravity(moons_dim, velocities_dim)
            apply_velocity(moons_dim, velocities_dim)

            steps[dim] += 1
            
            if matches_start_state(moons, velocities, moons_dim, velocities_dim, dim):
                break
    
    return calculate_lcm(steps)

result = solve()
print(f"Solution: {result}")