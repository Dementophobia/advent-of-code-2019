from aoc import read_file, timer

def manhattan(pos):
    return abs(pos[0]) + abs(pos[1])

def get_wire_positions(wire):
    x, y = 0, 0   
    positions = set()

    for i in range(len(wire)):
        for _ in range(int(wire[i][1:])):
            direction = wire[i][0]
            
            if   direction == "R":
                x +=1
            elif direction == "L":
                x -=1
            elif direction == "D":
                y +=1
            elif direction == "U":
                y -=1
            
            positions.add((x, y))
    
    return positions

@timer
def solve():
    input = read_file("03")
    wire_1 = input[0].split(",")
    wire_2 = input[1].split(",")
    
    positions_1 = get_wire_positions(wire_1)
    positions_2 = get_wire_positions(wire_2)

    crossings = positions_1.intersection(positions_2)
    
    return min([manhattan(pos) for pos in crossings])

result = solve()
print(f"Solution: {result}")