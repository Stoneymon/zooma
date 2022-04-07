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
        self.animals.append(animal)
        animal.care_taker = self.employee_id

    def remove_animal(self, animal):
        self.animals.remove(animal)