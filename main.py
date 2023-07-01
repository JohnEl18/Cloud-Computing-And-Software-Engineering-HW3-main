from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import HTTPException

from Menu import Menu

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

menu = Menu()


class Dishes(Resource):
    global menu

    def post(self):
        requests_parser = reqparse.RequestParser()

        try:
            requests_parser.add_argument("content-type", location="headers")
            requests_parser.add_argument("name", location="json")
            arguments = requests_parser.parse_args()
        except HTTPException as e:
            return 0, 415

        if arguments["content-type"] != "application/json":
            return 0, 415

        if arguments["name"] is None:
            return -1, 422

        dish_name = arguments["name"]
        added_dish_id = menu.add_dish(dish_name)

        if added_dish_id == -2:
            return -2, 422
        elif added_dish_id == -3:
            return -3, 422
        elif added_dish_id == -4:
            return -4, 504
        elif added_dish_id == -5:
            return -5, 502
        elif added_dish_id > 0:
            return added_dish_id, 201
        else:
            return "Unexpected error has occurred", 500

    def get(self):
        return menu.find_all_dishes(), 200

    def delete(self):
        return "This method is not allowed for the requested URL", 405


class Dish(Resource):
    global menu

    def get(self, key):
        dish_id = None
        if key.isdecimal():
            dish_id = int(key)
        dish = menu.find_dish(dish_name=key, dish_id=dish_id)
        if dish == {}:
            return -5, 404
        return dish, 200

    def delete(self, key):
        dish_id = None
        if key.isdecimal():
            dish_id = int(key)
        removed_dish_id = menu.remove_dish(dish_name=key, dish_id=dish_id)
        if removed_dish_id == -5:
            return -5, 404
        return removed_dish_id, 200


class Meals(Resource):
    global menu

    def post(self):
        requests_parser = reqparse.RequestParser()

        try:
            requests_parser.add_argument("content-type", location="headers")
            requests_parser.add_argument("name", location="json")
            requests_parser.add_argument("appetizer", location="json")
            requests_parser.add_argument("main", location="json")
            requests_parser.add_argument("dessert", location="json")
            arguments = requests_parser.parse_args()
        except HTTPException as e:
            return 0, 415

        if arguments["content-type"] != "application/json":
            return 0, 415

        if arguments["name"] is None or arguments["appetizer"] is None or arguments["main"] is None or \
                arguments["dessert"] is None:
            return -1, 422

        if not arguments["appetizer"].isdecimal() or not arguments["main"].isdecimal() or \
                not arguments["dessert"].isdecimal():
            return -1, 422

        meal_name = arguments["name"]
        appetizer_id = int(arguments["appetizer"])
        main_id = int(arguments["main"])
        dessert_id = int(arguments["dessert"])
        added_meal_id = menu.add_meal(meal_name, appetizer_id, main_id, dessert_id)

        if added_meal_id == -2:
            return -2, 422
        elif added_meal_id == -6:
            return -6, 422
        elif added_meal_id > 0:
            return added_meal_id, 201
        else:
            return "Unexpected error has occurred", 500

    def get(self):
        return menu.find_all_meals(), 200


class Meal(Resource):
    global menu

    def get(self, key):
        meal_id = None
        if key.isdecimal():
            meal_id = int(key)
        meal = menu.find_meal(meal_name=key, meal_id=meal_id)
        if meal == {}:
            return -5, 404
        return meal, 200

    def delete(self, key):
        meal_id = None
        if key.isdecimal():
            meal_id = int(key)
        removed_meal_id = menu.remove_meal(meal_name=key, meal_id=meal_id)
        if removed_meal_id == -5:
            return -5, 404
        return removed_meal_id, 200

    def put(self, key):
        meal_id = None
        if key.isdecimal():
            meal_id = int(key)
        else:
            return -1, 422

        requests_parser = reqparse.RequestParser()

        try:
            requests_parser.add_argument("content-type", location="headers")
            requests_parser.add_argument("name", location="json")
            requests_parser.add_argument("appetizer", location="json")
            requests_parser.add_argument("main", location="json")
            requests_parser.add_argument("dessert", location="json")
            arguments = requests_parser.parse_args()
        except HTTPException as e:
            return 0, 415

        if arguments["content-type"] != "application/json":
            return 0, 415

        if arguments["name"] is None or arguments["appetizer"] is None or arguments["main"] is None or \
                arguments["dessert"] is None:
            return -1, 422

        if not arguments["appetizer"].isdecimal() or not arguments["main"].isdecimal() or \
                not arguments["dessert"].isdecimal():
            return -1, 422

        meal_name = arguments["name"]
        appetizer_id = int(arguments["appetizer"])
        main_id = int(arguments["main"])
        dessert_id = int(arguments["dessert"])
        updated_meal_id = menu.update_meal(meal_id, meal_name, appetizer_id, main_id, dessert_id)

        if updated_meal_id == -6:
            return -6, 422
        elif updated_meal_id > 0:
            return updated_meal_id, 200
        else:
            return "Unexpected error has occurred", 500


api.add_resource(Dishes, "/dishes")
api.add_resource(Dish, '/dishes/<key>')
api.add_resource(Meals, "/meals")
api.add_resource(Meal, '/meals/<key>')

if __name__ == '__main__':
    #test commit
    # create collection dictionary and keys list
    print("running rest-word-svr-v1.py")
    # run Flask app.   default part is 5000
    app.run(host='0.0.0.0', port=8000, debug=True)
