from aoc import read_file, timer

def greatest_common_divisor(x, y):
    if not x:
        return abs(y)
    if not y:
        return abs(x)
    
    while y:
        x, y = y, x % y
    return abs(x)        

# Get all directions where an asteroid can be seen from station
def get_directions(station, asteroids):
    directions = set()
    for asteroid in asteroids:
        if asteroid == station:
            continue
                    
        vec = (asteroid[0] - station[0], asteroid[1] - station[1])
        gcd = greatest_common_divisor(vec[0], vec[1])
        vec = (vec[0] // gcd, vec[1] // gcd)
        
        directions.add(vec)
        
    return directions

@timer
def solve():
    input = read_file("10")
    size_x, size_y = len(input[0]), len(input)
    
    asteroids = [(x, y) for y in range(size_y) for x in range(size_x) if input[y][x] == "#"]
    
    return max([len(get_directions(station, asteroids)) for station in asteroids])

result = solve()
print(f"Solution: {result}")


