class Classroom:
    def __init__(self):
        self.students=[]

    def add_student(self,name):
        self.students.append(name)

    def count_students(self):
        return len(self.students)        
    
c = Classroom()

c.add_student("Ali")
c.add_student("Sara")
c.add_student("Omar")

print("Total students:", c.count_students())  
print("Students list:", c.students)    