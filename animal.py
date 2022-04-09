import uuid 
import datetime
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = []
        self.medical_record = []
        self.enclosure = None 
        self.care_taker = None
        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self): 
        self.feeding_record.append(datetime.datetime.now())

    def medical_checkup(self):
        self.medical_record.append(datetime.datetime.now())

    def gives_birth(self, zoo):
        #creates a child animal that shares the mother's species name and common name
        child = Animal(self.species_name, self.common_name, 0)
        if self.enclosure:
            #child gets put into the same enclosure as mother animal
            enclosure = zoo.get_enclosure(self.enclosure)
            enclosure.add_animal(child)
        #child gets put into zoo
        zoo.addAnimal(child)
        return child

    def dies(self, zoo):
        #animal gets removed from zoo and from enclosure
        if self.enclosure:
            enclosure = zoo.get_enclosure(self.enclosure)
            enclosure.animals.remove(self)
        if self.care_taker:
            employee = zoo.get_employee(self.care_taker)
            employee.remove_animal(self)
        zoo.removeAnimal(self)