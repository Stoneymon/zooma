import datetime
import random
class Zoo:
    def __init__ (self): 
        self.animals = []
        self.enclosures = []
        self.employees = []
        self.cleaning_plan = {}
        self.medical_plan = {}
        self.feeding_plan = {}

    def addAnimal(self, animal): 
        self.animals.append(animal)
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id: 
                return animal

    def get_stats(self):
        stats = {}
        stats['animals per species'] = self.per_species()
        stats['average number of animals per enclosure'] = self.per_enclosure()
        stats['Number of enclosures with multiple species'] = self.multiple_species()
        stats['Space per animal in each enclosure'] = self.space_per_animal()
        return stats

    def per_species(self):
        specieslist = []
        for animal in self.animals:
            if animal.species_name not in specieslist:
                specieslist.append(animal.species_name)
        animals_per_species = {}
        for species in specieslist:
            animals_per_species[species] = 0
            for animal in self.animals:
                if animal.species_name == species:
                    animals_per_species[species] += 1
        return animals_per_species

    def per_enclosure(self):
        average_animals_per_enclosure = len(self.animals) / len(self.enclosures)
        return average_animals_per_enclosure

    def multiple_species(self):
        enclosures_with_multiple_species = 0
        for enclosure in self.enclosures:
            if enclosure.multiple_species():
                enclosures_with_multiple_species += 1
        return (enclosures_with_multiple_species)

    def space_per_animal(self):
        space_per_animal = {}
        for enclosure in self.enclosures:
            space_per_animal[enclosure.enclosure_id] = enclosure.space_per_animal()
        return space_per_animal

    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def get_enclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def remove_enclosure(self, enclosure):
        if len(self.enclosures) < 2:
            return (print("You have to create another enclosure first"))
        enclosurelist = []
        for enclosures in self.enclosures:
            if enclosures != enclosure:
                enclosurelist.append(enclosures)
        new_enclosure = random.choice(enclosurelist)
        new_enclosure.animals += enclosure.animals
        self.enclosures.remove(enclosure)

    def add_employee(self, employee):
        self.employees.append(employee)

    def get_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    def remove_employee(self, employee):
        if len(self.employees) < 2:
            return (print("You have to hire anothe employee first"))
        employeelist = []
        for employees in self.employees:
            if employees != employee:
                employeelist.append(employees)
        new_caretaker = random.choice(employeelist)
        for animal in employee.animals:
            new_caretaker.add_animal(animal)
        self.employees.remove(employee)

    def employee_stats(self):
        stats = {}
        number_of_animals = []
        for employee in self.employees:
            number_of_animals.append(len(employee.animals))
        stats['min'] = min(number_of_animals)
        stats['max'] = max(number_of_animals)
        number_of_animals_with_employee = 0
        for number in number_of_animals:
            number_of_animals_with_employee += number
        stats['average'] = number_of_animals_with_employee / len(self.employees)
        return stats

    def create_cp(self):
        for enclosure in self.enclosures:
            if enclosure.cleaning_record:
                last_cleaned = enclosure.cleaning_record[-1]
            else:
                last_cleaned = datetime.datetime.now()
            next = last_cleaned + datetime.timedelta(days = 3)
            next = f"{next.year}-{next.month}-{next.day}"
            self.cleaning_plan[enclosure.enclosure_id] = [next, random.choice(self.employees)]

    def create_mp(self):
        for animal in self.animals:
            if animal.medical_record:
                last_medical = animal.medical_record[-1]
            else:
                last_medical = datetime.datetime.now()
            next = last_medical + datetime.timedelta(days = 35)
            next = f"{next.year}-{next.month}-{next.day}"
            self.medical_plan[animal.animal_id] = next

    def create_fp(self):
        for animal in self.animals:
            if animal.feeding_record:
                last_fed = animal.feeding_record[-1]
            else:
                last_fed = datetime.datetime.now()
            next = last_fed + datetime.timedelta(days = 2)
            next = f"{next.year}-{next.month}-{next.day}"
            self.feeding_plan[animal.animal_id] = [next, animal.care_taker]