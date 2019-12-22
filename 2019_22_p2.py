from aoc import read_file, timer
from collections import deque

def apply_operation(operations, addi, multi, size):
    operation = operations.popleft()
    
    if len(operations):
        addi, multi = apply_operation(operations, addi, multi, size)

    if operation[-2] == "cut":
        addi  += int(operation[-1]) * multi
    elif operation[-1] == "stack":
        multi *= -1
        addi  += multi
    else:
        multi *= pow(int(operation[-1]), -1, size)
    
    return addi, multi

@timer
def solve():
    input = read_file("22")
    operations = deque(reversed([line.split(" ") for line in input]))

    position    = 2020
    size        = 119315717514047
    iterations  = 101741582076661
    
    addi, multi = apply_operation(operations, 0, 1, size)
    
    all_multi   = pow(multi, iterations, size)
    all_addi    = addi * (1 - pow(multi, iterations, size)) * pow(1 - multi, -1, size)    

    return (position * all_multi + all_addi) % size

result = solve()
print(f"Solution: {result}")