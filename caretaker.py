import uuid
class Caretaker:
    def __init__(self, name, address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = []

    def remove(self, other):
        other.animals += self.animals

    def add_animal(self, animal):
        #puts an animal into the caretakers list of animals and sets the animal's care_taker value to the employees id
        self.animals.append(animal)
        animal.care_taker = self.employee_id

    def remove_animal(self, animal):
        #removes an animal from caretakers list of animals
        self.animals.remove(animal)