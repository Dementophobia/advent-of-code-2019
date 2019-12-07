from aoc import read_file, timer
from itertools import permutations

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes):
    mode_a, mode_b, mode_c = modes
    values = []
    
    if op in ["01", "02", "04", "05", "06", "07", "08"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        else:
            values.append(input[pos+1])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            else:
                values.append(input[pos+2])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                else:
                    values.append(input[pos+3])

    return values
    
def run_amp(phase, input, prog):
    input_counter = 0
    ip = 0

    while prog[ip] != 99:
        op, modes = split_instruction(prog[ip])
        values = get_values(prog, ip, op, modes)
        
        if op == "01": # Addition
            prog[prog[ip+3]] = values[0] + values[1]
            ip += 4
    
        if op == "02": # Multiplication
            prog[prog[ip+3]] = values[0] * values[1]
            ip += 4
        
        if op == "03": # Read and Store prog
            if not input_counter:
                prog[prog[ip+1]] = phase
            else:
                prog[prog[ip+1]] = input
            input_counter += 1
            ip += 2

        if op == "04": # Print Output
            output = values[0]
            ip += 2

        if op == "05": # Jump-if-True
            if values[0]:
                ip = values[1]
            else:
                ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                ip = values[1]
            else:
                ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                prog[prog[ip+3]] = 1
            else:
                prog[prog[ip+3]] = 0
            ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                prog[prog[ip+3]] = 1
            else:
                prog[prog[ip+3]] = 0
            ip += 4
    return output


def solve():
    prog = read_file("07")[0].split(",")
    prog = [int(x) for x in prog]

    max_thrust = 0

    for phases in permutations(range(5), 5):
        output = 0

        for phase in phases:
            output = run_amp(phase, output, prog)
        max_thrust = max(max_thrust, output)

    return max_thrust

result = solve()
print(f"Solution: {result}")