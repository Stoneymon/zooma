import pytest
import requests
import json
import datetime

from animal import Animal
from enclosure import Enclosure
from caretaker import Caretaker

@pytest.fixture
def baseURL ():
    return "http://127.0.0.1:7890"

@pytest.fixture
def tiger1 ():
    return Animal("tiger mum", "btiger1", 21)

@pytest.fixture
def tiger2 ():
    return Animal("tiger child", "btiger2", 2)

@pytest.fixture
def post_tiger1 (baseURL, tiger1):
    tiger1_data = {"species": tiger1.species_name, "name": tiger1.common_name, "age": tiger1.age}
    requests.post(baseURL + "/animal", data=tiger1_data)

@pytest.fixture
def enclosure1():
    return Enclosure("tigercage", 300)

@pytest.fixture
def post_enclosure1(baseURL, enclosure1):
    enclosure1_data = {"name": enclosure1.name, "area": enclosure1.area}
    requests.post(baseURL + "/enclosure", data=enclosure1_data)

@pytest.fixture
def employee1():
    return Caretaker('Caretaker1', 'Address1')

@pytest.fixture
def post_employee1(baseURL, employee1):
    employee1_data = {'name': employee1.name, 'address': employee1.address}
    requests.post(baseURL + '/employee', data=employee1_data)

class Testzoo ():

    def test_one(self, baseURL, post_tiger1):
        #animals
        x = requests.get(baseURL+"/animals")
        js = x.content
        animals = json.loads(js)
        assert (len(animals) == 1)

    def test_two(self, baseURL):
        #/animal/{animal_id}/vet
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/vet")
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)
        #check if the animals medical_record has an entry now
        assert(len(animals[0]['medical_record']) == 1)

    def test_three(self, baseURL):
        #/animal/{animal_id}/feed
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/feed")
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)

        #check if the animals feeding record has an entry now
        assert(len(animals[0]['feeding_record']) == 1)

    def test_four(self, baseURL):
        #/animal/{animal_id} GET
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        r = requests.get(baseURL + "/animal/" + animal['animal_id'])
        js = r.content
        animals = json.loads(js)
        #check if the function returned the correct animal
        assert(animals['species_name'] == 'tiger mum')
        assert(animals['common_name'] == 'btiger1')
        assert(animals['age'] == 21)

    def test_five(self, baseURL, post_enclosure1):
        #/enclosures
        x = requests.get(baseURL + "/enclosures")
        js = x.content
        enclosures = json.loads(js)
        #check if the add enclosure function worked
        assert(len(enclosures) == 1)

    def test_six(self, baseURL):
        #/animal/{animal_id}/home
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]

        #pass the data needed to the API call
        homedata = {"enclosure_id": enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)

        #update the animal and enclosure data
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]

        #check if the enclosure in the animal object is updated
        assert(animal['enclosure'] == enclosure['enclosure_id'])
        #check if the animal is added to the enclosure objects list of animals
        assert(len(enclosure['animals']) == 1)

        #test moving the animal to another enclosure
        #create the new enclosure
        enclosure2_data = {"name": 'enclosure2', "area": 400}
        requests.post(baseURL + "/enclosure", data=enclosure2_data)

        new_enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[1]
        new_homedata = {"enclosure_id": new_enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=new_homedata)

        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        new_enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[1]
        old_enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        # check if the enclosure in the animal object is updated
        assert(animal['enclosure'] == new_enclosure['enclosure_id'])
        # check if the animal is added to the new enclosure objects list of animals
        assert(len(new_enclosure['animals']) == 1)
        #check if animal is removed from old enclosure
        assert(len(old_enclosure['animals']) == 0)



    def test_seven(self, baseURL):
        #/animal/birth
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]

        #pass the mother_id to the API call
        birthdata = {"mother_id": animal['animal_id']}
        requests.post(baseURL + "/animal/birth", data=birthdata)

        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[1]
        animals = json.loads(requests.get(baseURL + "/animals").content)

        #check if the "child animal" has been added to the enclosure and to the zoo
        assert(len(enclosure['animals']) == 2)
        assert(len(animals) == 2)

        #check if common_name, species_name and enclosure are the same as the mothers
        assert(animals[0]['species_name'] == animals[1]['species_name'])
        assert(animals[0]['common_name'] == animals[1]['common_name'])
        assert(animals[1]['age'] == 0)
        assert(animals[0]['enclosure'] == animals[1]['enclosure'])

    def test_eight(self, baseURL):
        #/animal/death
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]

        #pass the id of the animal that died to the API call
        deathdata = {'animal_id': animal['animal_id']}
        requests.post(baseURL + "/animal/death", data=deathdata)

        #check if animal got removed from the zoo and from the enclosure
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert(len(animals) == 1)
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[1]
        assert(len(enclosure['animals']) == 1)

    def test_nine(self, baseURL):
        #/animal/{animal_id} DELETE
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)
        assert(len(animals) == 1)
        requests.delete(baseURL + "/animal/" + animal['animal_id'])
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)
        assert(len(animals) == 0)

    def test_ten(self, baseURL, post_tiger1, tiger2):
        #/animals/stat
        #since there are no animals left, I created a new one and put it into an enclosure
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        homedata = {"enclosure_id": enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)

        #and I created a second one through the birth function
        birthdata = {"mother_id": animal['animal_id']}
        requests.post(baseURL + "/animal/birth", data=birthdata)
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert(len(animals)==2)

        #and a third one so i have an enclosure with multiple species
        animaldata = {"species": tiger2.species_name, "name": tiger2.common_name, "age": tiger2.age}
        requests.post(baseURL + "/animal", data=animaldata)
        animal = json.loads(requests.get(baseURL + "/animals").content)[2]
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)

        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        enclosure2 = json.loads(requests.get(baseURL + "/enclosures").content)[1]
        stats = json.loads(requests.get(baseURL + "/animals/stat").content)
        #two animals of species 'tiger mum', one of species 'tiger child'
        assert(stats['animals per species']['tiger mum'] == 2)
        assert(stats['animals per species']['tiger child'] == 1)
        #2 enclosures, 3 animals
        assert(stats['average number of animals per enclosure'] == 1.5)
        #one enclosure with 2 species
        assert(stats['Number of enclosures with multiple species'] == 1)
        assert(stats['Space per animal in each enclosure'][enclosure['enclosure_id']] == 100)
        #no animals in that enclosure
        assert(stats['Space per animal in each enclosure'][enclosure2['enclosure_id']] == 'no animals')



    def test_eleven(self, baseURL):
        #/enclosures/{enclosure_id}/clean
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        requests.post(baseURL + "/enclosures/" + enclosure['enclosure_id'] + "/clean")
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert(len(enclosure['cleaning_record']) == 1)

    def test_twelve(self, baseURL):
        #/enclosures/{enclosure_id}/animals
        #3 animals are supposed to be in that enclosure 2x species tiger mum, 1x species tiger child
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert(len(enclosure['animals']) == 3)
        enclosure_animals = json.loads(requests.get(baseURL + "/enclosures/" + enclosure['enclosure_id'] + "/animals").content)
        assert(enclosure_animals[0]['species_name'] == 'tiger mum')
        assert(enclosure_animals[0]['age'] == 21)
        assert(enclosure_animals[1]['species_name'] == 'tiger mum')
        assert(enclosure_animals[1]['age'] == 0)
        assert(enclosure_animals[2]['species_name'] == 'tiger child')
        assert(enclosure_animals[2]['age'] == 2)

    def test_thirteen(self, baseURL):
        #/enclosure/{enclosure_id}
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)
        #3 animals in the enclosure at position 0
        assert(len(enclosures[0]['animals']) == 3)
        #no animals in the other enclosure
        assert(len(enclosures[1]['animals']) == 0)
        #delete the enclosure at position 0
        requests.delete(baseURL + "/enclosure/" + enclosures[0]['enclosure_id'])
        enclosures = json.loads(requests.get(baseURL + "/enclosures").content)
        #all the animals are in the one enclosure that's left
        assert(len(enclosures) == 1)
        assert(len(enclosures[0]['animals']) == 3)

    def test_fourteen(self, baseURL, post_employee1):
        #/employees
        r = requests.get(baseURL + "/employees")
        js = r.content
        employees = json.loads(js)
        assert(len(employees) == 1)

    def test_fifteen(self, baseURL):
        #/employee/{employee_id}/care/{animal_id}
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        animal = json.loads(requests.get(baseURL + '/animals').content)[0]

        requests.post(baseURL + '/employee/' + employee['employee_id'] + '/care/' + animal['animal_id'])

        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        animal = json.loads(requests.get(baseURL + '/animals').content)[0]

        #check if the animal is in the employees animals list now and if the animals care_taker value is the employees id
        assert(employee['animals'][0] == animal)
        assert(animal['care_taker'] == employee['employee_id'])

    def test_sixteen(self, baseURL):
        #/employee/{employee_id}/care/animals
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        employee_animals = json.loads(requests.get(baseURL + '/employee/' + employee['employee_id'] + '/care/animals').content)

        #employee takes care of one animal
        assert(len(employee_animals) == 1)
        assert (employee_animals[0]['species_name'] == 'tiger mum')
        assert (employee_animals[0]['age'] == 21)

        #add another animal to check
        animal = json.loads(requests.get(baseURL + '/animals').content)[2]
        requests.post(baseURL + '/employee/' + employee['employee_id'] + '/care/' + animal['animal_id'])
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        employee_animals = json.loads(requests.get(baseURL + '/employee/' + employee['employee_id'] + '/care/animals').content)

        #employee takes care of 2 animals now
        assert(len(employee_animals) == 2)
        assert (employee_animals[1]['species_name'] == 'tiger child')
        assert (employee_animals[1]['age'] == 2)

    def test_seventeen(self, baseURL):
        #/employees/stats
        #add another employee with 1 animal to take care of
        employee2_data = {'name': 'Caretaker2', 'address': 'Address2'}
        requests.post(baseURL + '/employee', data=employee2_data)
        employee = json.loads(requests.get(baseURL + '/employees').content)[1]
        animal = json.loads(requests.get(baseURL + '/animals').content)[1]
        requests.post(baseURL + '/employee/' + employee['employee_id'] + '/care/' + animal['animal_id'])

        stats = json.loads(requests.get(baseURL + '/employees/stats').content)
        assert(stats['min'] == 1)
        assert(stats['max'] == 2)
        assert(stats['average'] == 1.5)

    def test_eighteen(self, baseURL):
        #/employee/{employee_id}
        employees = json.loads(requests.get(baseURL + '/employees').content)
        #zoo has 2 employees, one takes care of 2 animals, the other one takes care of one animal
        assert(len(employees) == 2)
        assert(len(employees[0]['animals']) == 2)
        assert(len(employees[1]['animals']) == 1)

        #delete one employee, animals get transfered to the other employee
        requests.delete(baseURL + '/employee/' + employees[0]['employee_id'])
        employees = json.loads(requests.get(baseURL + '/employees').content)

        #check if employee takes care of 3 animals now
        assert(len(employees[0]['animals']) == 3)
        #check if animals 'care_taker' value got updated
        assert(employees[0]['animals'][1]['care_taker'] == employees[0]['employee_id'])
        #check if employee got removed from zoos employee list
        assert(len(employees) == 1)

    def test_nineteen(self, baseURL):
        #/tasks/cleaning
        enclosure_data = {"name": 'Enclosure', "area": 160}
        requests.post(baseURL + "/enclosure", data=enclosure_data)
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)

        #only clean one enclosure to see if function works with an empty cleaning_record
        requests.post(baseURL + "/enclosures/" + enclosures[0]['enclosure_id'] + "/clean")
        cleaning_plan = json.loads(requests.get(baseURL + '/tasks/cleaning').content)
        assert(len(cleaning_plan) == 2)

        #check if the dates are correct and if there is an employee that has to clean the enclosure
        next = datetime.datetime.now() + datetime.timedelta(days=3)
        next = f"{next.year}-{next.month}-{next.day}"
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]

        assert(cleaning_plan[enclosures[0]['enclosure_id']] == [next, employee])
        assert(cleaning_plan[enclosures[1]['enclosure_id']] == [next, employee])

    def test_twenty(self, baseURL):
        #/tasks/medical
        #function works the same way as cleaning_plan
        animals = json.loads(requests.get(baseURL + '/animals').content)
        assert(len(animals) == 3)

        medical_plan = json.loads(requests.get(baseURL + '/tasks/medical').content)
        next = datetime.datetime.now() + datetime.timedelta(days=35)
        next = f"{next.year}-{next.month}-{next.day}"

        assert(medical_plan[animals[0]['animal_id']] == next)
        assert(medical_plan[animals[1]['animal_id']] == next)
        assert(medical_plan[animals[2]['animal_id']] == next)

    def test_twentyone(self, baseURL):
        #/tasks/feeding
        # function works the same way as cleaning_plan
        animals = json.loads(requests.get(baseURL + '/animals').content)
        feeding_plan = json.loads(requests.get(baseURL + '/tasks/feeding').content)

        next = datetime.datetime.now() + datetime.timedelta(days=2)
        next = f"{next.year}-{next.month}-{next.day}"
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]

        assert(len(employee['animals']) == 3)
        assert(feeding_plan[animals[0]['animal_id']] == [next, employee['employee_id']])
        assert(feeding_plan[animals[1]['animal_id']] == [next, employee['employee_id']])
        assert(feeding_plan[animals[2]['animal_id']] == [next, employee['employee_id']])