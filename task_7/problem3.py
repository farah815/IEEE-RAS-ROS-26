class Passenger:
     def __init__(self,name):
         self.name=name
       


class Flight(Passenger):
    def __init__(self):
        self.passengers=[]

    def add_passenger(self,passenger_obj):
        self.passengers.append(passenger_obj)       
         
p1 = Passenger("Ali")
p2 = Passenger("Sara")
p3 = Passenger("Omar")

f = Flight()

f.add_passenger(p1)
f.add_passenger(p2)
f.add_passenger(p3)

# Display passengers in the flight
for p in f.passengers:
    print(p.name)
    