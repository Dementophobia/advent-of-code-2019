from aoc import read_file, timer

def cut(deck, amount):
    if amount > 0:
        return deck[amount:] + deck[:amount]
    elif amount < 0:
        return deck[len(deck)+amount:] + deck[:len(deck)+amount]
    return deck

def deal_into_new_stack(deck):
    return deck[::-1]

def deal_with_increment(deck, amount):
    new_deck = [0 for _ in range(len(deck))]
    for i in range(len(deck)):
        new_deck[(i*amount)%len(deck)] = deck[i]
    return new_deck

@timer
def solve():
    input = read_file("22")
    instructions = [line.split(" ") for line in input]

    deck = [num for num in range(10007)]
    
    for instruction in instructions:
        if instruction[-2] == "cut":
            deck = cut(deck, int(instruction[-1]))
            
        elif instruction[-1] == "stack":
            deck = deal_into_new_stack(deck)
       
        else:
            deck = deal_with_increment(deck, int(instruction[-1]))

    return deck.index(2019)

result = solve()
print(f"Solution: {result}")