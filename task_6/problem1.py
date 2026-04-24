class Dog:
    def __init__(self,name,breed):
        self.name=name
        self.breed=breed

    def bark(self):
        print(f"Woof!My name is {self.name}") 
        
dog1 = Dog("Buddy", "Golden Retriever")
dog1.bark()           