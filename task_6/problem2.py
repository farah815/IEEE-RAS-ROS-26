class calculator:
    def add(self,a,b):
        return a+b
    
    def subtract(self,a,b):
        return a-b
    
    def multiply(self,a,b):
        return a*b
calc = calculator()

print(f"addition result is {calc.add(5, 3)}")
print(f"subtraction result is {calc.subtract(10, 4)}")
print(f"multiplication result is {calc.multiply(2,6)}")    