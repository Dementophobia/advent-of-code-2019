from aoc import read_file, timer

def num_below(field, level, pos):
    if pos[0] == 1:
        return sum(field[level-1][0][x] == "#" for x in range(5))
    
    if pos[0] == 3:
        return sum(field[level-1][4][x] == "#" for x in range(5))
    
    if pos[1] == 1:
        return sum(field[level-1][y][0] == "#" for y in range(5))
                
    if pos[1] == 3:
        return sum(field[level-1][y][4] == "#" for y in range(5))
                
    

def num_neighbors(field, level, pos):
    count = 0

    for side in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        new_pos = (pos[0] + side[0], pos[1] + side[1])

        if new_pos[0] == 2 and new_pos[1] == 2:
            count += num_below(field, level, pos)
                    
        elif new_pos[0] == -1:
            if field[level+1][1][2] == "#":
                count += 1
        
        elif new_pos[0] == 5:
            if field[level+1][3][2] == "#":
                count += 1

        elif new_pos[1] == -1:
            if field[level+1][2][1] == "#":
                count += 1
        
        elif new_pos[1] == 5:
            if field[level+1][2][3] == "#":
                count += 1
                    
        elif field[level][new_pos[0]][new_pos[1]] == "#":
            count += 1

    return count

def evolve(field, iterations):
    new_field = [[["." for x in range(5)] for y in range(5)] for z in range(iterations*2+3)]
    
    for level in range(iterations*2+1):
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    continue
        
                if field[level][y][x] == "#":
                    if num_neighbors(field, level, (y, x)) == 1:
                        new_field[level][y][x] = "#"

                else:
                    if num_neighbors(field, level, (y, x)) == 1 or num_neighbors(field, level, (y, x)) == 2:
                        new_field[level][y][x] = "#"

    return new_field
    
@timer
def solve():
    input = read_file("24")
    iterations = 200
    field = [[["." for x in range(5)] for y in range(5)] for z in range(iterations*2+3)]

    for y in range(5):
        for x in range(5):
            field[iterations+1][y][x] = input[y][x]

    for step in range(iterations):
        field = evolve(field, iterations)
    
    return sum(field[level][y][x] == "#" for level in range(iterations*2+3) for y in range(5) for x in range(5))

result = solve()
print(f"Solution: {result}")