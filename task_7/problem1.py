class Animal:
    def speak(self):
        print("general sound")

class Dog(Animal):
    def speak(self):
        print("Woof")


general= Animal()
general.speak()   

dog = Dog()
dog.speak()