from aoc import read_file, timer

def get_pos(orbits, planet):
    pos = 0
    while planet in orbits.keys():
        planet = orbits[planet]
        pos += 1
    return pos 

def get_all_planets(input):
    return set(planet for line in input for planet in line.split(")"))

def generate_orbit_dict(input):
    orbits = {}
    
    for line in input:
        planets = line.split(")")
        orbits[planets[1]] = planets[0]
    
    return orbits

def solve():
    input = read_file("06")

    orbits      = generate_orbit_dict(input)
    all_planets = get_all_planets(input)

    return sum(get_pos(orbits, k) for k in all_planets)

result = solve()
print(f"Solution: {result}")
