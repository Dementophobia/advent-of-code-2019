from aoc import read_file, timer

def increases(num):
    num = list(str(num))
    
    if num == sorted(num):
        return True
    return False

def all_digits_unique(num):
    num = str(num)
    return len(num) == len(set(num))

@timer
def solve():
    input = read_file("04")
    start, end = [int(num) for num in input[0].split("-")]

    return sum(increases(num) and not all_digits_unique(num) for num in range(start, end+1))

result = solve()
print(f"Solution: {result}")