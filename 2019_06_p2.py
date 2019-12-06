from aoc import read_file, timer

def get_planet_position(orbits, planet):
    pos = 0
    while planet in orbits.keys():
        planet = orbits[planet]
        pos += 1
    return pos  
  
def get_planets(orbits, positions, planet):
    planets = []
    
    while planet in orbits.keys():
        planet = orbits[planet]
        planets.append(planet)
        
    return planets

def get_all_planets(input):
    return set(planet for line in input for planet in line.split(")"))

def get_all_positions(all_planets, orbits):
    positions = {}
    
    for planet in all_planets:
        positions[planet] = get_planet_position(orbits, planet)
    
    return positions

def generate_orbit_dict(input):
    orbits = dict()
    
    for line in input:
        planets = line.split(")")
        orbits[planets[1]] = planets[0]
    
    return orbits

def solve():
    input = read_file("06")

    orbits      = generate_orbit_dict(input)
    all_planets = get_all_planets(input)
    positions   = get_all_positions(all_planets, orbits)

    san = get_planets(orbits, positions, "SAN")
    you = get_planets(orbits, positions, "YOU")
    
    maximum = max(positions[planet] for planet in set(san).intersection(set(you)))

    return positions["SAN"] + positions["YOU"] - 2 * maximum - 2

result = solve()
print(f"Solution: {result}")
