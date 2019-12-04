from aoc import read_file, timer

def increases(num):
    num = list(str(num))
    
    if num == sorted(num):
        return True
    return False

def has_double(num):
    num = list(str(num))
    
    for i in range(5):
        if num[i] == num[i+1] and \
          (i == 0 or num[i] != num[i-1]) and \
          (i == 4 or num[i] != num[i+2]):
            return True
    return False

@timer
def solve():
    input = read_file("04")
    start, end = [int(num) for num in input[0].split("-")]

    return sum(increases(num) and has_double(num) for num in range(start, end+1))

result = solve()
print(f"Solution: {result}")
