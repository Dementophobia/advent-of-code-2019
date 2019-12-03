from aoc import read_file, timer
from collections import defaultdict

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

def get_distance_for_crossings(wire, crossings):
    crossing = defaultdict(int)
    distance = 0
    x, y = 0, 0
    
    for i in range(len(wire)):
        for _ in range(int(wire[i][1:])):
            if wire[i][0] == "R":
                x +=1
            elif wire[i][0] == "L":
                x -=1
            elif wire[i][0] == "D":
                y +=1
            elif wire[i][0] == "U":
                y -=1
            
            distance += 1
            
            if (x, y) in crossings:
                crossing[(x, y)] = distance

    return crossing

@timer
def solve():
    input = read_file("03")
    wire_1 = input[0].split(",")
    wire_2 = input[1].split(",")

    x1, y1, x2, y2 = 0, 0, 0, 0

    positions_1 = get_wire_positions(wire_1)
    positions_2 = get_wire_positions(wire_2)

    crossings = positions_1.intersection(positions_2)

    crossing_distance_1 = get_distance_for_crossings(wire_1, crossings)
    crossing_distance_2 = get_distance_for_crossings(wire_2, crossings)

    return min([crossing_distance_1[crossing] + crossing_distance_2[crossing] for crossing in crossings])

result = solve()
print(f"Solution: {result}")