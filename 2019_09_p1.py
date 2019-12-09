from aoc import read_file, timer
from collections import defaultdict

class Booster:
    def __init__(self, prog):
        self.prog     = prog
        self.ip       = 0
        self.output   = 0
        self.rel_base = 0

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes, booster):
    mode_a, mode_b, mode_c = modes
    values = []
    offset = 0
    
    if op in ["01", "02", "04", "05", "06", "07", "08", "09"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        elif mode_c == "1":
            values.append(input[pos+1])
        elif mode_c == "2":
            values.append(input[input[pos+1]+booster.rel_base])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            elif mode_b == "1":
                values.append(input[pos+2])
            elif mode_b == "2":
                values.append(input[input[pos+2]+booster.rel_base])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                elif mode_a == "1":
                    values.append(input[pos+3])
                elif mode_a == "2":
                    values.append(input[input[pos+3]+booster.rel_base])

    if op in ["01", "02", "07", "08"]:
        if mode_a == "2":
            offset = booster.rel_base
    
    if op in ["03"]:
        if mode_c == "2":
            offset = booster.rel_base

    return values, offset
  
def run_booster(input, booster):
    while booster.prog[booster.ip] != 99:
        op, modes = split_instruction(booster.prog[booster.ip])
        values, offset = get_values(booster.prog, booster.ip, op, modes, booster)
        
        if op == "01": # Addition
            booster.prog[booster.prog[booster.ip+3] + offset] = values[0] + values[1]
            booster.ip += 4
    
        if op == "02": # Multiplication
            booster.prog[booster.prog[booster.ip+3] + offset] = values[0] * values[1]
            booster.ip += 4
        
        if op == "03": # Read and Store input
            booster.prog[booster.prog[booster.ip+1] + offset] = input
            booster.ip += 2

        if op == "04": # Print Output
            booster.output = values[0]
            print(booster.output)
            booster.ip += 2

        if op == "05": # Jump-if-True
            if values[0]:
                booster.ip = values[1]
            else:
                booster.ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                booster.ip = values[1]
            else:
                booster.ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                booster.prog[booster.prog[booster.ip+3] + offset] = 1
            else:
                booster.prog[booster.prog[booster.ip+3] + offset] = 0
            booster.ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                booster.prog[booster.prog[booster.ip+3] + offset] = 1
            else:
                booster.prog[booster.prog[booster.ip+3] + offset] = 0
            booster.ip += 4

        if op == "09": # Adjust Relative Base
            booster.rel_base += values[0]
            booster.ip += 2
    
    return booster

def create_program(input):
    prog = defaultdict(int)
    
    for i in range(len(input)):
        prog[i] = int(input[i])
    
    return prog

@timer
def solve():
    input = read_file("09")[0].split(",")
    prog = create_program(input)

    booster = Booster(prog)
    booster = run_booster(1, booster)

    return(booster.output)

result = solve()
print(f"Solution: {result}")
       
