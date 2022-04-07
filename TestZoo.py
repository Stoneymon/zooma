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
        assert (len(animals)==1)

    def test_two(self, baseURL):
        #/animal/{animal_id}/vet
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/vet")
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)
        assert(animals[0]['species_name'] == 'tiger mum')
        assert(len(animals[0]['medical_record']) == 1)

    def test_three(self, baseURL):
        #/animal/{animal_id}/feed
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/feed")
        r = requests.get(baseURL + "/animals")
        js = r.content
        animals = json.loads(js)
        assert(animals[0]['species_name'] == 'tiger mum')
        assert(len(animals[0]['feeding_record']) == 1)

    def test_four(self, baseURL):
        #/animal/{animal_id} GET
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        r = requests.get(baseURL + "/animal/" + animal['animal_id'])
        js = r.content
        animals = json.loads(js)
        assert(animals['species_name'] == 'tiger mum')
        assert(animals['common_name'] == 'btiger1')
        assert(animals['age'] == 21)

    def test_five(self, baseURL, post_enclosure1):
        #/enclosures
        x = requests.get(baseURL + "/enclosures")
        js = x.content
        enclosures = json.loads(js)
        assert(len(enclosures) == 1)

    def test_six(self, baseURL):
        #/animal/{animal_id}/home
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        homedata = {"enclosure_id": enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert(animal['enclosure'] == enclosure['enclosure_id'])
        assert(len(enclosure['animals'])==1)
        assert(enclosure['animals'][0]['species_name'] == 'tiger mum')

    def test_seven(self, baseURL):
        #/animal/birth
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        homedata = {"enclosure_id": enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        birthdata = {"mother_id": animal['animal_id']}
        requests.post(baseURL + "/animal/birth", data=birthdata)
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert(len(enclosure['animals'])==2)
        assert(len(animals)==2)
        assert(animals[0]['species_name'] == animals[1]['species_name'])
        assert(animals[0]['common_name'] == animals[1]['common_name'])
        assert(animals[1]['age'] == 0)
        assert(animals[0]['enclosure'] == animals[1]['enclosure'])

    def test_eight(self, baseURL):
        #/animal/death
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert (len(animals) == 2)
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert (len(enclosure['animals']) == 2)
        deathdata = {'animal_id': animal['animal_id']}
        requests.post(baseURL + "/animal/death", data=deathdata)
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert(len(animals) == 1)
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
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

    def test_ten(self, baseURL, post_tiger1):
        #/animal/stat
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        homedata = {"enclosure_id": enclosure['enclosure_id'], "animal_id": animal['animal_id']}
        requests.post(baseURL + "/animal/" + animal['animal_id'] + "/home", data=homedata)
        animal = json.loads(requests.get(baseURL + "/animals").content)[0]
        birthdata = {"mother_id": animal['animal_id']}
        requests.post(baseURL + "/animal/birth", data=birthdata)
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        animals = json.loads(requests.get(baseURL + "/animals").content)
        assert(len(animals) == 2)
        assert(len(enclosure['animals']) == 2)
        stats = json.loads(requests.get(baseURL + "/animals/stat").content)
        assert(stats['animals per species']['tiger mum'] == 2)
        assert(stats['average number of animals per enclosure'] == 2)
        assert(stats['Number of enclosures with multiple species'] == 0)
        assert(stats['Space per animal in each enclosure'][enclosure['enclosure_id']] == 150)


    def test_eleven(self, baseURL):
        #/enclosures/{enclosure_id}/clean
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        requests.post(baseURL + "/enclosures/" + enclosure['enclosure_id'] + "/clean")
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert(len(enclosure['cleaning_record']) == 1)

    def test_twelve(self, baseURL, post_tiger1):
        #/enclosures/{enclosure_id}/animals
        enclosure = json.loads(requests.get(baseURL + "/enclosures").content)[0]
        assert(len(enclosure['animals']) == 2)
        enclosure_animals = json.loads(requests.get(baseURL + "/enclosures/" + enclosure['enclosure_id'] + "/animals").content)
        assert(enclosure_animals[0]['species_name'] == 'tiger mum')
        assert(enclosure_animals[0]['common_name'] == 'btiger1')
        assert(enclosure_animals[0]['age'] == 21)
        assert(enclosure_animals[1]['species_name'] == 'tiger mum')
        assert(enclosure_animals[1]['common_name'] == 'btiger1')
        assert(enclosure_animals[1]['age'] == 0)

    def test_thirteen(self, baseURL):
        #/enclosure/{enclosure_id}
        enclosure2_data = {'name': 'enclosure2', 'area': 150}
        requests.post(baseURL + '/enclosure', data=enclosure2_data)
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)
        assert(len(enclosures) == 2)
        assert(len(enclosures[1]['animals']) == 0)
        assert(enclosures[1]['name'] == 'enclosure2')
        assert(len(enclosures[0]['animals']) == 2)
        assert(enclosures[0]['name'] == 'tigercage')
        requests.delete(baseURL + "/enclosure/" + enclosures[0]['enclosure_id'])
        enclosures = json.loads(requests.get(baseURL + "/enclosures").content)
        assert(len(enclosures) == 1)
        assert(enclosures[0]['name'] == 'enclosure2')
        assert(len(enclosures[0]['animals']) == 2)

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
        assert(employee['animals'][0] == animal)
        assert(animal['care_taker'] == employee['employee_id'])

    def test_sixteen(self, baseURL):
        #/employee/{employee_id}/care/animals
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        employee_animals = json.loads(requests.get(baseURL + '/employee/' + employee['employee_id'] + '/care/animals').content)
        assert(len(employee_animals) == 1)
        assert (employee_animals[0]['species_name'] == 'tiger mum')
        assert (employee_animals[0]['common_name'] == 'btiger1')
        assert (employee_animals[0]['age'] == 21)
        animal = json.loads(requests.get(baseURL + '/animals').content)[1]
        requests.post(baseURL + '/employee/' + employee['employee_id'] + '/care/' + animal['animal_id'])
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        employee_animals = json.loads(requests.get(baseURL + '/employee/' + employee['employee_id'] + '/care/animals').content)
        assert(len(employee_animals) == 2)
        assert (employee_animals[1]['species_name'] == 'tiger mum')
        assert (employee_animals[1]['common_name'] == 'btiger1')
        assert (employee_animals[1]['age'] == 0)

    def test_seventeen(self, baseURL):
        #/employees/stats
        stats = json.loads(requests.get(baseURL + '/employees/stats').content)
        assert(stats['min'] == 2)
        assert(stats['max'] == 2)
        assert(stats['average'] == 2)

    def test_eighteen(self, baseURL):
        #/employee/{employee_id}
        employee2_data = {'name': 'Caretaker2', 'address': 'Address2'}
        requests.post(baseURL + '/employee', data=employee2_data)
        employees = json.loads(requests.get(baseURL + '/employees').content)
        assert(len(employees) == 2)
        assert(len(employees[0]['animals']) == 2)
        assert(employees[0]['name'] == 'Caretaker1')
        assert(len(employees[1]['animals']) == 0)
        requests.delete(baseURL + '/employee/' + employees[0]['employee_id'])
        employees = json.loads(requests.get(baseURL + '/employees').content)
        assert(employees[0]['animals'][0]['care_taker'] == employees[0]['employee_id'])
        assert(len(employees) == 1)
        assert(len(employees[0]['animals']) == 2)
        assert(employees[0]['name'] == 'Caretaker2')

    def test_nineteen(self, baseURL):
        #/tasks/cleaning
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)
        assert(len(enclosures) == 1)
        requests.post(baseURL + "/enclosures/" + enclosures[0]['enclosure_id'] + "/clean")
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)
        assert(len(enclosures[0]['cleaning_record']) == 1)
        enclosure_data = {"name": 'Enclosure', "area": 160}
        requests.post(baseURL + "/enclosure", data=enclosure_data)
        enclosures = json.loads(requests.get(baseURL + '/enclosures').content)
        assert(len(enclosures) == 2)
        assert(len(enclosures[1]['cleaning_record']) == 0)
        cleaning_plan = json.loads(requests.get(baseURL + '/tasks/cleaning').content)
        assert(len(cleaning_plan) == 2)
        next = datetime.datetime.now() + datetime.timedelta(days=3)
        next = f"{next.year}-{next.month}-{next.day}"
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        assert(cleaning_plan[enclosures[0]['enclosure_id']] == [next, employee])
        assert(cleaning_plan[enclosures[1]['enclosure_id']] == [next, employee])

    def test_twenty(self, baseURL):
        #/tasks/medical
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
        animals = json.loads(requests.get(baseURL + '/animals').content)
        feeding_plan = json.loads(requests.get(baseURL + '/tasks/feeding').content)
        next = datetime.datetime.now() + datetime.timedelta(days=2)
        next = f"{next.year}-{next.month}-{next.day}"
        employee = json.loads(requests.get(baseURL + '/employees').content)[0]
        assert(len(employee['animals']) == 2)
        assert(feeding_plan[animals[0]['animal_id']] == [next, employee['employee_id']])
        assert(feeding_plan[animals[1]['animal_id']] == [next, employee['employee_id']])
        assert(feeding_plan[animals[2]['animal_id']] == [next, None])