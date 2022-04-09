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
        #adds animal into enclosures list of animals and sets animals enclosure value to enclosures id
        self.animals.append(animal)
        animal.enclosure = self.enclosure_id

    def remove_animal(self, animal):
        #removes animal from enclosures list of animals
        self.animals.remove(animal)

    def multiple_species(self):
        #checks if there are animals of different species in the enclosure
        if not self.animals:
            return False
        species1 = self.animals[0].species_name
        for i in range(1, len(self.animals)):
            if self.animals[i].species_name != species1:
                return True

    def space_per_animal(self):
        #checks the available space per animal
        if self.animals:
            return (self.area/len(self.animals))
        else:
            return "no animals"