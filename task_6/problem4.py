class Rectangle :
    def __init__ (self,width,height):
        self.width=width
        self.height=height

    def getarea(self):
        return self.width*self.height    

rec = Rectangle(5,10)
print(f"area of rectangle is {rec.getarea()}")