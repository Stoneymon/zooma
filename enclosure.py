import uuid
import datetime
from animal import Animal
class Enclosure:
    def __init__(self, name, area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.area = area
        self.animals = []
        self.cleaning_record = []

    def clean(self):
        self.cleaning_record.append(datetime.datetime.now())

    def add_animal(self, animal):
        self.animals.append(animal)
        animal.enclosure = self.enclosure_id

    def remove_animal(self, animal):
        self.animals.remove(animal)

    def multiple_species(self):
        if not self.animals:
            return False
        species1 = self.animals[0].species_name
        for i in range(1, len(self.animals)):
            if self.animals[i].species_name != species1:
                return True

    def space_per_animal(self):
        if self.animals:
            return (self.area/len(self.animals))
        else:
            return "no animals"