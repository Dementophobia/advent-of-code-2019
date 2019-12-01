import time

def read_file(name):
    with open(f"files/input{name}") as f:
        content = f.readlines()
    return [x.strip() for x in content]

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"\nTime required: {(time.time() - start_time)*1000:.2f} ms\n")
        return result
    return wrapper