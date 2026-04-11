import random

def Pick_Winner(names) :
    if len(names)==0:
        return "THE LIST IS ALREADY EMPTY!"
    
    Winner= random.choice(names)
    return("CONGRATULAION " +  Winner + " YOU ARE THE WINNER!")

names_list = ["Ali", "Sara", "Omar", "Mona"]
result = Pick_Winner(names_list)
print(result)