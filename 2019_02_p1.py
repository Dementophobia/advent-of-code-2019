from aoc import read_file, timer

@timer
def solve():
    input = read_file("02")[0].split(",")
    input = [int(x) for x in input]

    pos = 0
    input[1] = 12
    input[2] = 2

    while input[pos] != 99:
        if input[pos] == 1:
            input[input[pos+3]] = input[input[pos+1]] + input[input[pos+2]]
    
        if input[pos] == 2:
            input[input[pos+3]] = input[input[pos+1]] * input[input[pos+2]]

        pos += 4
    
    return input[0]

result = solve()
print(f"Solution: {result}")