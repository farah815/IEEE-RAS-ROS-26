import random

def get_unique_lottery():
    numbers = set()

    while len(numbers) < 6:
        numbers.add(random.randint(1, 50))

    return numbers
print(get_unique_lottery())