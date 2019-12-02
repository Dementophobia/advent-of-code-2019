from aoc import read_file, timer

@timer
def solve():
    input       = read_file("02")[0].split(",")
    input_store = [int(x) for x in input]

    for noun in range(100):
        for verb in range(100):
            input = input_store[:]
            pos = 0
            input[1] = noun
            input[2] = verb

            while input[pos] != 99:
                if input[pos] == 1:
                    input[input[pos+3]] = input[input[pos+1]] + input[input[pos+2]]
    
                if input[pos] == 2:
                    input[input[pos+3]] = input[input[pos+1]] * input[input[pos+2]]

                pos += 4
    
            if input[0] == 19690720:
                return 100 * noun + verb

result = solve()
print(f"Solution: {result}")