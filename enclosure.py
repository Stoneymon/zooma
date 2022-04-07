import uuid
import datetime
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

    def remove_animal(self, animal):
        self.animals.remove(animal)

    def multiple_species(self):
        species1 = self.animals[0].species_name
        for i in range(1, len(self.animals)):
            if self.animals[i].species_name != species1:
                return True
        return False

    def space_per_animal(self):
        return (self.area/len(self.animals))