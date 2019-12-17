from aoc import read_file, timer
from collections import defaultdict

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
  
def run_game(game, input = 10):
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

def error_message(game):
    print(chr(game.output), end = "")
    while not game.halt:
        print(chr(run_game(game).output), end = "")

@timer
def solve():
    input  = read_file("17")[0].split(",")
    input[0] = 2
    prog   = create_program(input)
    game   = Game(prog)
    
    field = defaultdict(str)
    x, y = 0, 0
    
    while not game.halt and y < 30:
        run_game(game, 0)
        if game.output == 10:
            print()
            y += 1
            x = 0
        else:
            print(chr(game.output), end = "")
            field[(x, y)] = chr(game.output)
            x += 1

    instructions = []
    instructions.append([ord(c) for c in "A,C,B,C,A,B,A,B,C\n"])
    instructions.append([ord(c) for c in "L,12,R,4,R,4,R,12\n"])
    instructions.append([ord(c) for c in "L,10,L,6,R,4\n"])
    instructions.append([ord(c) for c in "L,12,R,4,R,4,L,6\n"])
    instructions.append([ord(c) for c in "n\n"])

    while run_game(game).output != 10:
        print(chr(game.output), end = "")
    print()

    for inst in instructions:
        for num in inst:
            print(f"Input: {num} / {chr(num)}")
        
            run_game(game, num)
        
            if game.output != 10:
                error_message(game)
                break
        if game.halt:
            break

    return 0

result = solve()
print(f"Solution: {result}")

