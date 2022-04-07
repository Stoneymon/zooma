import pytest
import datetime

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure
from caretaker import Caretaker


@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger", "ti", 2)

@pytest.fixture
def panther1():
    return Animal("panther", "panth", 5)

@pytest.fixture
def zoo1 ():
    return Zoo ()

@pytest.fixture
def enclosure1():
    return Enclosure("Tigercage", 150)

@pytest.fixture
def caretaker1():
    return Caretaker("Melvin", "India")

def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert(tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    assert(len(zoo1.animals)==2)

def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.feed()

    assert(len(tiger1.feeding_record)==1)

def test_medical_checkup(tiger1):
    tiger1.medical_checkup()

    assert(len(tiger1.medical_record) == 1)

def test_add_enclosure(zoo1):
    zoo1.add_enclosure(enclosure1)

    assert(len(zoo1.enclosures)==1)

def test_set_home(tiger1, enclosure1):
    tiger1.new_enclosure(enclosure1.enclosure_id)
    assert (tiger1.enclosure == enclosure1.enclosure_id)
    enclosure1.add_animal(tiger1)
    assert(len(enclosure1.animals)==1)

# def test_change_home(tiger1, enclosure1):
#     tiger1.new_enclosure(enclosure1.enclosure_id)
#     assert(tiger1.enclosure == enclosure1.enclosure_id)
#     enclosure1.add_animal(tiger1)
#     assert(len(enclo))

def test_birth(tiger1, enclosure1, zoo1):
    zoo1.addAnimal(tiger1)
    zoo1.add_enclosure(enclosure1)
    tiger1.new_enclosure(enclosure1.enclosure_id)
    enclosure1.add_animal(tiger1)
    child = tiger1.gives_birth(zoo1)

    assert(len(enclosure1.animals)==2)
    assert(len(zoo1.animals)==2)
    assert(child.species_name == tiger1.species_name)
    assert(child.common_name == tiger1.common_name)
    assert(child.age == 0)

def test_death(tiger1, enclosure1, zoo1):
    zoo1.addAnimal(tiger1)
    zoo1.add_enclosure(enclosure1)
    tiger1.new_enclosure(enclosure1.enclosure_id)
    enclosure1.add_animal(tiger1)
    tiger1.dies(zoo1)

    assert(len(zoo1.animals)==0)
    assert(len(enclosure1.animals)==0)

def test_stat(tiger1, tiger2, panther1, enclosure1, zoo1, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(panther1)
    zoo1.add_enclosure(enclosure1)
    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure1.add_animal(panther1)
    zoo1.add_employee(caretaker1)
    caretaker1.add_animal(tiger1)
    caretaker1.add_animal(tiger2)
    caretaker1.add_animal(panther1)

    assert(zoo1.get_stats()['animals per species']['tiger'] == 2)
    assert(zoo1.get_stats()['animals per species']['panther'] == 1)
    assert(zoo1.get_stats()['average number of animals per enclosure'] == 3)
    assert(zoo1.get_stats()['Number of enclosures with multiple species'] == 1)
    assert(zoo1.get_stats()['Space per animal in each enclosure'][enclosure1.enclosure_id] == 50)

def test_cleaning_enclosure(zoo1, enclosure1):
    zoo1.add_enclosure(enclosure1)
    enclosure1.clean()

    assert(len(enclosure1.cleaning_record)==1)

def test_remove_enclosure(zoo1, enclosure1, tiger1, tiger2, panther1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(panther1)
    zoo1.add_enclosure(enclosure1)
    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure2 = Enclosure("Enclosure2", 300)
    zoo1.add_enclosure(enclosure2)
    enclosure2.add_animal(panther1)

    zoo1.remove_enclosure(enclosure1)
    assert(len(zoo1.enclosures)==1)
    assert(len(enclosure2.animals)==3)

def test_add_employee(zoo1, caretaker1):
    zoo1.add_employee(caretaker1)

    assert(len(zoo1.employees)==1)

def test_set_employee(caretaker1, tiger1):
    caretaker1.add_animal(tiger1)

    assert(len(caretaker1.animals)==1)
    assert(tiger1.care_taker == caretaker1.employee_id)

def test_employee_stats(zoo1, caretaker1, tiger1, tiger2, panther1, enclosure1):
    caretaker2 = Caretaker("Ekbal", "Vienna")
    caretaker3 = Caretaker("Dominik", "Bosnia")
    zoo1.add_employee(caretaker1)
    zoo1.add_employee(caretaker2)
    zoo1.add_employee(caretaker3)
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(panther1)
    zoo1.add_enclosure(enclosure1)
    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure1.add_animal(panther1)
    caretaker1.add_animal(tiger1)
    caretaker1.add_animal(tiger2)
    caretaker2.add_animal(panther1)

    assert(zoo1.employee_stats()['min'] == 0)
    assert(zoo1.employee_stats()['max'] == 2)
    assert(zoo1.employee_stats()['average'] == 1)

def test_remove_employee(zoo1, caretaker1, tiger1, tiger2, panther1):
    caretaker2 = Caretaker("Ekbal", "Vienna")
    zoo1.add_employee(caretaker1)
    zoo1.add_employee(caretaker2)
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(panther1)
    caretaker1.add_animal(tiger1)
    caretaker1.add_animal(tiger2)
    caretaker2.add_animal(panther1)

    zoo1.remove_employee(caretaker1)

    assert(len(zoo1.employees) == 1)
    assert(len(caretaker2.animals) == 3)

def test_cleaning_plan(zoo1, enclosure1, caretaker1):
    enclosure2 = Enclosure("Enclosure2", 300)
    zoo1.add_employee(caretaker1)
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    enclosure1.clean()

    zoo1.create_cp()

    next = datetime.datetime.now() + datetime.timedelta(days=3)
    next = f"{next.year}-{next.month}-{next.day}"
    assert(zoo1.cleaning_plan[enclosure1.enclosure_id] == [next, caretaker1])
    assert(zoo1.cleaning_plan[enclosure2.enclosure_id] == [next, caretaker1])

def test_medical_plan(zoo1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    tiger1.medical_checkup()

    zoo1.create_mp()

    next = datetime.datetime.now() + datetime.timedelta(days=35)
    next = f"{next.year}-{next.month}-{next.day}"
    assert(zoo1.medical_plan[tiger1.animal_id] == next)
    assert(zoo1.medical_plan[tiger2.animal_id] == next)

def test_feeding_plan(zoo1, tiger1, tiger2, caretaker1):
    caretaker2 = Caretaker("Ekbal", "Vienna")
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.add_employee(caretaker1)
    zoo1.add_employee(caretaker2)
    caretaker1.add_animal(tiger1)
    caretaker2.add_animal(tiger2)
    tiger1.feed()

    zoo1.create_fp()

    next = datetime.datetime.now() + datetime.timedelta(days=2)
    next = f"{next.year}-{next.month}-{next.day}"
    assert(zoo1.feeding_plan[tiger1.animal_id] == [next, caretaker1.employee_id])
    assert(zoo1.feeding_plan[tiger2.animal_id] == [next, caretaker2.employee_id])