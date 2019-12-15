from aoc import read_file, timer
from collections import defaultdict
from copy import copy


class Grid:
    def __init__(self, content = int):
        self.grid = defaultdict(content)
        self.pos = (0, 0)
    
    def up(self):
        self.pos = (self.pos[0], self.pos[1]+1)
    
    def right(self):
        self.pos = (self.pos[0]+1, self.pos[1])
    
    def down(self):
        self.pos = (self.pos[0], self.pos[1]-1)
    
    def left(self):
        self.pos = (self.pos[0]-1, self.pos[1])

    def set_pos(self, value):
        self.grid[self.pos] = value

    def wallbounce(self, direction):
        if direction == "up":
            self.up()
            self.set_pos("#")
            self.down()
        elif direction == "down":
            self.down()
            self.set_pos("#")
            self.up()
        elif direction == "left":
            self.left()
            self.set_pos("#")
            self.right()
        elif direction == "right":
            self.right()
            self.set_pos("#")
            self.left()

    def search(self, value):
        for k, v in self.grid.items():
            if v == value:
                return k

    def get_border(self):
        top, right, bottom, left = -1e8, -1e8, 1e8, 1e8
        for position, value in self.grid.items():
            if value:
                top     = max(top, position[1])
                right   = max(right, position[0])
                bottom  = min(bottom, position[1])
                left    = min(left, position[0])
        return top, right, bottom, left

    def draw(self):
        top, right, bottom, left = self.get_border()
        for y in range(bottom, top+1):
            for x in range(left, right+1):
                print(self.grid[(x, y)], end="")
                if self.grid[(x, y)] == "":
                    print(" ", end="")
            print()
    
class Game:
    def __init__(self, prog):
        self.prog     = prog
        self.ip       = 0
        self.output   = 0
        self.rel_base = 0
        self.halt     = False

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes, game):
    mode_a, mode_b, mode_c = modes
    values = []
    offset = 0
    
    if op in ["01", "02", "04", "05", "06", "07", "08", "09"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        elif mode_c == "1":
            values.append(input[pos+1])
        elif mode_c == "2":
            values.append(input[input[pos+1]+game.rel_base])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            elif mode_b == "1":
                values.append(input[pos+2])
            elif mode_b == "2":
                values.append(input[input[pos+2]+game.rel_base])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                elif mode_a == "1":
                    values.append(input[pos+3])
                elif mode_a == "2":
                    values.append(input[input[pos+3]+game.rel_base])

    if op in ["01", "02", "07", "08"]:
        if mode_a == "2":
            offset = game.rel_base
    
    if op in ["03"]:
        if mode_c == "2":
            offset = game.rel_base

    return values, offset
  
def run_game(game, input = 0):
    while game.prog[game.ip] != 99:
        op, modes = split_instruction(game.prog[game.ip])
        values, offset = get_values(game.prog, game.ip, op, modes, game)
        
        if op == "01": # Addition
            game.prog[game.prog[game.ip+3] + offset] = values[0] + values[1]
            game.ip += 4
    
        if op == "02": # Multiplication
            game.prog[game.prog[game.ip+3] + offset] = values[0] * values[1]
            game.ip += 4
        
        if op == "03": # Read and Store input
            game.prog[game.prog[game.ip+1] + offset] = input
            game.ip += 2

        if op == "04": # Print Output
            game.output = values[0]
            game.ip += 2
            return game

        if op == "05": # Jump-if-True
            if values[0]:
                game.ip = values[1]
            else:
                game.ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                game.ip = values[1]
            else:
                game.ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                game.prog[game.prog[game.ip+3] + offset] = 1
            else:
                game.prog[game.prog[game.ip+3] + offset] = 0
            game.ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                game.prog[game.prog[game.ip+3] + offset] = 1
            else:
                game.prog[game.prog[game.ip+3] + offset] = 0
            game.ip += 4

        if op == "09": # Adjust Relative Base
            game.rel_base += values[0]
            game.ip += 2
    
    game.halt = True
    return game

def create_program(input):
    prog = defaultdict(int)
    
    for i in range(len(input)):
        prog[i] = int(input[i])
    
    return prog

def get_best_dir(field, visited):
    all_dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    
    for dir in all_dirs:
        new_pos = (field.pos[0] + dir[0], field.pos[1] + dir[1])
        if field.grid[new_pos] != "":
            continue

        d = all_dirs.index(dir)+1
        return d
    
    least_visited = 1e8
    least_dir = -1
    
    for dir in all_dirs:
        new_pos = (field.pos[0] + dir[0], field.pos[1] + dir[1])
        if field.grid[new_pos] == "#":
            continue
        
        if least_visited > visited[new_pos]:
            least_dir = dir
            least_visited = visited[new_pos]
            
    d = all_dirs.index(least_dir) + 1
    return d

def get_map(game):
    visited = defaultdict(int)
    field = Grid(str)
    steps = 0
    
    while not game.halt and steps < 6000:
        dir = get_best_dir(field, visited)
        steps += 1
        run_game(game, dir)
        
        if game.output == 0:
            field.wallbounce(["up", "down", "left", "right"][dir-1])
        
        if game.output == 1:
            [field.up, field.down, field.left, field.right][dir-1]()
            field.set_pos(".")
        
        if game.output == 2:
            [field.up, field.down, field.left, field.right][dir-1]()
            field.set_pos("O")
        
        visited[field.pos] += 1
        
    return field

def find_oxygen(field):
    search = defaultdict(int)
    search[(0, 0)] = 1
    new_search = copy(search)
    top, right, bottom, left = field.get_border()
    steps = 0
    
    while True:
        steps += 1
        for y in range(bottom, top+1):
            for x in range(left, right+1):
                if search[(x, y)] == 1:
                    new_search[(x, y)] = -1
                    for dir in [(-1, 0),(0, -1),(1, 0),(0, 1)]:
                        new_pos = (x + dir[0], y + dir[1])
                        if search[new_pos] == -1:
                            continue
                        if field.grid[new_pos] == ".":
                            new_search[new_pos] = 1
                        if field.grid[new_pos] == "O":
                            return steps
        
        search = copy(new_search)
 
@timer
def solve():
    input  = read_file("15")[0].split(",")
    prog   = create_program(input)
    game   = Game(prog)
    field  = get_map(game)
    
    return find_oxygen(field)

result = solve()
print(f"Solution: {result}")