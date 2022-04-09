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
        #calls the different stats functions and puts them into a dictionary
        stats = {}
        stats['animals per species'] = self.per_species()
        stats['average number of animals per enclosure'] = self.per_enclosure()
        stats['Number of enclosures with multiple species'] = self.multiple_species()
        stats['Space per animal in each enclosure'] = self.space_per_animal()
        return stats

    def per_species(self):
        #returns the number of animals of each species in the zoo
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
        #returns the average number of animals per enclosure
        if self.enclosures:
            average_animals_per_enclosure = len(self.animals) / len(self.enclosures)
            return average_animals_per_enclosure
        else:
            return None

    def multiple_species(self):
        #returns the number of enclosures with animals from different species
        enclosures_with_multiple_species = 0
        for enclosure in self.enclosures:
            if enclosure.multiple_species():
                enclosures_with_multiple_species += 1
        return (enclosures_with_multiple_species)

    def space_per_animal(self):
        #returns the available space per animal for each enclosure
        space_per_animal = {}
        for enclosure in self.enclosures:
            space_per_animal[enclosure.enclosure_id] = enclosure.space_per_animal()
        return space_per_animal

    def add_enclosure(self, enclosure):
        #adds an enclosure to the zoo's list of enclosures
        self.enclosures.append(enclosure)

    def get_enclosure(self, enclosure_id):
        #returns the enclosure with the specified enclosure id
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def set_enclosure(self, animal, enclosure):
        #puts animal into specified enclosure, removes it from it's old enclosure if there is one
        if animal.enclosure:
            old_enclosure = self.get_enclosure(animal.enclosure)
            old_enclosure.remove_animal(animal)
        enclosure.add_animal(animal)

    def remove_enclosure(self, enclosure):
        #removes the specified enclosure (only if there is at least one other enclosure in the zoo)
        if len(self.enclosures) < 2:
            return None
        #creates list of enclosures without the enclosure that gets deleted
        enclosurelist = []
        for enclosures in self.enclosures:
            if enclosures != enclosure:
                enclosurelist.append(enclosures)
        #picks a new enclosure randomly, and puts the animals that were in the deleted enclosure into the chosen enclosure
        new_enclosure = random.choice(enclosurelist)
        new_enclosure.animals += enclosure.animals
        self.enclosures.remove(enclosure)
        return True

    def add_employee(self, employee):
        #adds an employee to the zoos list of employees
        self.employees.append(employee)

    def get_employee(self, employee_id):
        #returns the employee with the specified employee id
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    def remove_employee(self, employee):
        #removes the specified employee (only if there is at least one other employee)
        if len(self.employees) < 2:
            return None
        #chooses new employee
        employeelist = []
        for employees in self.employees:
            if employees != employee:
                employeelist.append(employees)
        new_caretaker = random.choice(employeelist)
        #puts animals of deleted employee into chosen employees list of animals
        for animal in employee.animals:
            new_caretaker.add_animal(animal)
        self.employees.remove(employee)
        return True

    def employee_stats(self):
        stats = {}
        #gets the numbers of animals each employee takes care of
        number_of_animals = []
        for employee in self.employees:
            number_of_animals.append(len(employee.animals))
        if number_of_animals:
            stats['min'] = min(number_of_animals)
            stats['max'] = max(number_of_animals)
            stats['average'] = len(self.animals) / len(self.employees)
            return stats
        else:
            return None

    def create_cp(self):
        #creates a dictionary with all enclosures, the next time they get cleaned and a randomly chosen employee
        #that has to clean it
        for enclosure in self.enclosures:
            if enclosure.cleaning_record:
                last_cleaned = enclosure.cleaning_record[-1]
            else:
                last_cleaned = datetime.datetime.now()
            next = last_cleaned + datetime.timedelta(days = 3)
            next = f"{next.year}-{next.month}-{next.day}"
            if self.employees:
                self.cleaning_plan[enclosure.enclosure_id] = [next, random.choice(self.employees)]
            else:
                self.cleaning_plan[enclosure.enclosure_id] = [next, 'no employees']

    def create_mp(self):
        #creates a dictionary with all animals and the next time they have to go to the vet
        for animal in self.animals:
            if animal.medical_record:
                last_medical = animal.medical_record[-1]
            else:
                last_medical = datetime.datetime.now()
            next = last_medical + datetime.timedelta(days = 35)
            next = f"{next.year}-{next.month}-{next.day}"
            self.medical_plan[animal.animal_id] = next

    def create_fp(self):
        #creates a dictionary with all animals and the next time they get fed and the employee that has to feed them
        for animal in self.animals:
            if animal.feeding_record:
                last_fed = animal.feeding_record[-1]
            else:
                last_fed = datetime.datetime.now()
            next = last_fed + datetime.timedelta(days = 2)
            next = f"{next.year}-{next.month}-{next.day}"
            self.feeding_plan[animal.animal_id] = [next, animal.care_taker]