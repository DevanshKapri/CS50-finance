class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def addPassenger(self, name):
        if not self.openSeats():
            return False
        else:
            self.passengers.append(name)
            return True
        
    def openSeats(self):
        return self.capacity - len(self.passengers)


flight = Flight(4)

people = ["Shubh", "Aryan", "Ram", "Sarvesh", "Tommy"]

for person in people:
    submit = flight.addPassenger(person)
    if submit:
        print(f"Reserved seat for {person}")
    else:
        print(f"No Seats available for {person}")
