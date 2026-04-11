def calculate_bill(prices, items_bought):
    total = 0

    for item in items_bought:
        if item in prices:
            total += prices[item]

    return total

prices = {
    "apple": 0.5,
    "banana": 0.3,
    "milk": 1.2,
    "bread": 2.0
}

items_bought = ["apple", "banana", "apple", "milk", "bread"]

result = calculate_bill(prices, items_bought)
print("Total bill =", result)