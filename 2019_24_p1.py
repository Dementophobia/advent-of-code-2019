from aoc import read_file, timer

def num_neighbors(field, pos):
    count = 0
    for side in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        x, y = pos[1] + side[1], pos[0] + side[0]
        if x >= 0 and x <= 4 and \
           y >= 0 and y <= 4 and \
           field[y][x] == "#":
                count += 1
    return count

def evolve(field):
    new_field = [["." for x in range(5)] for y in range(5)]
    
    for y in range(5):
        for x in range(5):
            if field[y][x] == "#":
                if num_neighbors(field, (y, x)) == 1:
                    new_field[y][x] = "#"
            elif num_neighbors(field, (y, x)) == 1 or \
                 num_neighbors(field, (y, x)) == 2:
                new_field[y][x] = "#"

    return new_field
    
def bio_diversity(field):
    result, multi = 0, 1
    
    for y in range(5):
        for x in range(5):
            if field[y][x] == "#":
                result += multi
            multi *= 2
    return result

@timer
def solve():
    field = read_file("24")
    known = set()
    
    while (bio := bio_diversity(field)) not in known:
        known.add(bio)
        field = evolve(field)

    return bio

result = solve()
print(f"Solution: {result}")