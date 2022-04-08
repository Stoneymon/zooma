from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo
from animal import Animal
from enclosure import Enclosure
from caretaker import Caretaker

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, help='The scientific name of the animal, e.g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True, help='Enclosure ID')

birth_parser = reqparse.RequestParser()
birth_parser.add_argument('mother_id', type=str, required=True, help='ID of the Mother')

death_parser = reqparse.RequestParser()
death_parser.add_argument('animal_id', type=str, required=True, help='Animal ID')

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help='The name of the Enclosure')
enclosure_parser.add_argument('area', type=int, required=True, help='Area of the Enclosure')

employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True, help='Name of the Caretaker')
employee_parser.add_argument('address', type=str, required=True, help='Address of the Caretaker')

care_parser = reqparse.RequestParser()
care_parser.add_argument('animal_id', type=str, required=True, help='Animal ID')


@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal (species, name, age) 
        #add the animal to the zoo
        my_zoo.addAnimal(new_animal)
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result = my_zoo.getAnimal(animal_id)
        return jsonify(search_result)
    
     def delete(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        enclosure_id = targeted_animal.enclosure
        if enclosure_id:
            enclosure = my_zoo.get_enclosure(enclosure_id)
            enclosure.remove_animal(targeted_animal)
        my_zoo.removeAnimal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")

@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify(my_zoo.animals)

@zooma_api.route('/animal/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)

@zooma_api.route('/animal/<animal_id>/vet')
class Medical_Checkup(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.medical_checkup()
        return jsonify(targeted_animal)

@zooma_api.route('/animal/<animal_id>/home')
class Home(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        new_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not new_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        my_zoo.set_enclosure(targeted_animal, new_enclosure)
        return jsonify(targeted_animal)


@zooma_api.route('/animal/birth')
class Birth(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):
        args = birth_parser.parse_args()
        mother_id = args['mother_id']
        mother = my_zoo.getAnimal(mother_id)
        if not mother:
            return jsonify(f"Animal with ID {mother_id} was not found")
        child = mother.gives_birth(my_zoo)
        return jsonify(child)

@zooma_api.route('/animal/death')
class Death(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['animal_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.dies(my_zoo)
        return jsonify(targeted_animal)

@zooma_api.route('/animals/stat')
class AnimalStats(Resource):
    def get(self):
        stats = my_zoo.get_stats()
        return jsonify(stats)

@zooma_api.route('/enclosure')
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        # get the post parameters
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        # create a new animal object
        new_enclosure = Enclosure(name, area)
        # add the animal to the zoo
        my_zoo.add_enclosure(new_enclosure)
        return jsonify(new_enclosure)

@zooma_api.route('/enclosures')
class AllEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.enclosures)

@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_enclosure.clean()
        return jsonify(targeted_enclosure)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class EnclosureAnimals(Resource):
    def get(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        return jsonify(targeted_enclosure.animals)

@zooma_api.route('/enclosure/<enclosure_id>')
class RemoveEnclosure(Resource):
    def delete(self, enclosure_id):
        if len(my_zoo.enclosures) < 2:
            return jsonify("Not enough enclosures")
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        if not my_zoo.remove_enclosure(targeted_enclosure):
            return jsonify("You need another enclosure.")
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")

@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        # get the post parameters
        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']
        # create a new animal object
        new_employee = Caretaker(name, address)
        # add the animal to the zoo
        my_zoo.add_employee(new_employee)
        return jsonify(new_employee)

@zooma_api.route('/employees')
class AllEmployees(Resource):
    def get(self):
        return jsonify(my_zoo.employees)

@zooma_api.route('/employee/<employee_id>/care/<animal_id>/')
class TakesCare(Resource):
    def post(self, employee_id, animal_id):
        targeted_employee = my_zoo.get_employee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        old_employee = my_zoo.get_employee(targeted_animal.care_taker)
        if old_employee:
            old_employee.remove_animal(targeted_animal)
        targeted_employee.add_animal(targeted_animal)
        return jsonify(targeted_animal)

@zooma_api.route('/employee/<employee_id>/care/animals')
class EmployeesAnimals(Resource):
    def get(self, employee_id):
        targeted_employee = my_zoo.get_employee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(targeted_employee.animals)

@zooma_api.route('/employees/stats')
class EmployeeStats(Resource):
    def get(self):
        return jsonify(my_zoo.employee_stats())

@zooma_api.route('/employee/<employee_id>')
class EmployeeID(Resource):
    def delete(self, employee_id):
        targeted_employee = my_zoo.get_employee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        if not my_zoo.remove_employee(targeted_employee):
            return jsonify("You have to hire another employee first.")
        return jsonify(f"Employee with ID {employee_id} was removed")

@zooma_api.route('/tasks/cleaning')
class CleaningPlan(Resource):
    def get(self):
        my_zoo.create_cp()
        return jsonify(my_zoo.cleaning_plan)

@zooma_api.route('/tasks/medical')
class MedicalPlan(Resource):
    def get(self):
        my_zoo.create_mp()
        return jsonify(my_zoo.medical_plan)

@zooma_api.route('/tasks/feeding')
class FeedingPlan(Resource):
    def get(self):
        my_zoo.create_fp()
        return jsonify(my_zoo.feeding_plan)


if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)