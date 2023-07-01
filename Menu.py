import requests
from numpy.random import uniform
from requests.exceptions import RequestException

nutrition_api_url_template = "https://api.api-ninjas.com/v1/nutrition?query={query}"
api_key = "VOdpDsYZ3vI7/tFchi7Ysw==v1W5MRGMULuR0PG5"


class Menu:
    def __init__(self):
        self.dishes = {}
        self.meals = {}

    def __retrieve_dish_nutrition(self, dish_name):
        try:
            response = requests.get(nutrition_api_url_template.format(query=dish_name), headers={"X-Api-Key": api_key})
        except RequestException as e:
            raise ConnectionError("Error connecting to nutrition api") from e

        if response.status_code == requests.codes.ok:
            try:
                dishes = response.json()
            except RequestException as e:
                raise ValueError("Error reading response content as json") from e
            return dishes

        raise ValueError(f"Unexpected response status code {response.status_code}")

    def __generate_id(self):
        return int(repr(uniform(0, 1))[2:])

    def __generate_dish_id(self):
        dish_id = self.__generate_id()
        while self.find_dish(dish_id=dish_id) != {}:
            dish_id = self.__generate_id()
        return dish_id

    def __generate_meal_id(self):
        meal_id = self.__generate_id()
        while self.find_meal(meal_id=meal_id) != {}:
            meal_id = self.__generate_id()
        return meal_id

    def find_dish(self, dish_name=None, dish_id=None):
        if dish_name is not None:
            for item_id, dish_properties in self.dishes.items():
                if dish_properties["name"] == dish_name:
                    return dish_properties
        if dish_id is not None:
            if dish_id in self.dishes.keys():
                return self.dishes[dish_id]
        return {}

    def find_meal(self, meal_name=None, meal_id=None):
        if meal_name is not None:
            for item_id, meal_properties in self.meals.items():
                if meal_properties["name"] == meal_name:
                    return meal_properties
        if meal_id is not None:
            if meal_id in self.meals.keys():
                return self.meals[meal_id]
        return {}

    def find_all_dishes(self):
        return self.dishes

    def find_all_meals(self):
        return self.meals

    def add_dish(self, name):
        """

        :param name:
        :return: -2 means that the dish is already exists
                 -3 means that the dish was not found in the nutrition api
                 -4 means that a connection error has occurred
                 -5 means that response unexpected content or status code received
        """
        dish_properties = {"name": name, "ID": None, "cal": 0, "size": 0, "sodium": 0, "sugar": 0}

        if self.find_dish(dish_name=name) != {}:
            return -2

        dish_properties["ID"] = self.__generate_dish_id()

        try:
            dishes = self.__retrieve_dish_nutrition(name)
        except ConnectionError as e:
            return -4
        except ValueError as e:
            return -5
        if len(dishes) == 0:
            return -3
        for dish in dishes:
            dish_properties["cal"] += dish["calories"]
            dish_properties["size"] += dish["serving_size_g"]
            dish_properties["sodium"] += dish["sodium_mg"]
            dish_properties["sugar"] += dish["sugar_g"]

        self.dishes[dish_properties["ID"]] = dish_properties
        return dish_properties["ID"]

    def remove_dish(self, dish_name=None, dish_id=None):
        """

        :param dish_name:
        :param dish_id:
        :return: -5 means that the requested dish is not found
        """
        dish = self.find_dish(dish_name=dish_name, dish_id=dish_id)
        if dish == {}:
            return -5
        removed_dish = self.dishes.pop(dish["ID"])
        removed_dish_id = removed_dish["ID"]

        for meal_id, meal_properties in self.meals.items():
            dish_found = False
            if removed_dish_id == meal_properties["appetizer"]:
                self.meals[meal_id]["appetizer"] = None
                dish_found = True
            if removed_dish_id == meal_properties["main"]:
                self.meals[meal_id]["main"] = None
                dish_found = True
            if removed_dish_id == meal_properties["dessert"]:
                self.meals[meal_id]["dessert"] = None
                dish_found = True
            if dish_found:
                self.__update_meal_nutrition(meal_id)

        return removed_dish["ID"]

    def remove_meal(self, meal_name=None, meal_id=None):
        """

        :param meal_name:
        :param meal_id:
        :return: -5 means that the requested meal is not found
        """
        meal = self.find_meal(meal_name=meal_name, meal_id=meal_id)
        if meal == {}:
            return -5
        removed_meal = self.meals.pop(meal["ID"])
        return removed_meal["ID"]

    def __calculate_meal_nutrition(self, appetizer, main, dessert):
        if appetizer is None:
            appetizer = {"cal": 0, "sodium": 0, "sugar": 0}
        if main is None:
            main = {"cal": 0, "sodium": 0, "sugar": 0}
        if dessert is None:
            dessert = {"cal": 0, "sodium": 0, "sugar": 0}

        meal_cal = appetizer["cal"] + main["cal"] + dessert["cal"]
        meal_sodium = appetizer["sodium"] + main["sodium"] + dessert["sodium"]
        meal_sugar = appetizer["sugar"] + main["sugar"] + dessert["sugar"]

        return meal_cal, meal_sodium, meal_sugar

    def __update_meal_nutrition(self, meal_id):
        if self.meals[meal_id]["appetizer"] is None:
            appetizer = {"cal": 0, "sodium": 0, "sugar": 0}
        else:
            appetizer = self.find_dish(dish_id=self.meals[meal_id]["appetizer"])
            if appetizer == {}:
                appetizer = {"cal": 0, "sodium": 0, "sugar": 0}
        if self.meals[meal_id]["main"] is None:
            main = {"cal": 0, "sodium": 0, "sugar": 0}
        else:
            main = self.find_dish(dish_id=self.meals[meal_id]["main"])
            if main == {}:
                main = {"cal": 0, "sodium": 0, "sugar": 0}
        if self.meals[meal_id]["dessert"] is None:
            dessert = {"cal": 0, "sodium": 0, "sugar": 0}
        else:
            dessert = self.find_dish(dish_id=self.meals[meal_id]["dessert"])
            if dessert == {}:
                dessert = {"cal": 0, "sodium": 0, "sugar": 0}

        self.meals[meal_id]["cal"], self.meals[meal_id]["sodium"], self.meals[meal_id][
            "sugar"] = self.__calculate_meal_nutrition(appetizer, main, dessert)

    def add_meal(self, name, appetizer_id, main_id, dessert_id):
        """

        :param name:
        :param appetizer_id:
        :param main_id:
        :param dessert_id:
        :return: -2 means that a meal with the requested name is already exists
                 -6 means that one of the sent dish IDs (appetizer, main, dessert) does not exist
        """
        meal_properties = {"name": name, "ID": None, "appetizer": None, "main": None, "dessert": None, "cal": 0,
                           "sodium": 0, "sugar": 0}

        if self.find_meal(meal_name=name) != {}:
            return -2

        meal_properties["ID"] = self.__generate_meal_id()
        appetizer = self.find_dish(dish_id=appetizer_id)
        main = self.find_dish(dish_id=main_id)
        dessert = self.find_dish(dish_id=dessert_id)

        if appetizer == {} or main == {} or dessert == {}:
            return -6

        meal_id = self.__generate_meal_id()

        meal_properties["ID"] = meal_id
        meal_properties["appetizer"] = appetizer["ID"]
        meal_properties["main"] = main["ID"]
        meal_properties["dessert"] = dessert["ID"]

        meal_properties["cal"], meal_properties["sodium"], meal_properties["sugar"] = self.__calculate_meal_nutrition(
            appetizer, main, dessert)

        self.meals[meal_properties["ID"]] = meal_properties

        return meal_properties["ID"]

    def update_meal(self, meal_id, meal_name, meal_appetizer_id, meal_main_id, meal_dessert_id):
        """

        :param meal_id:
        :param meal_name:
        :param meal_appetizer_id:
        :param meal_main_id:
        :param meal_dessert_id:
        :return: -6 means that the requested meal or one of the sent dish IDs (appetizer, main, dessert) does not exist
        """
        meal = self.find_meal(meal_id=meal_id)
        if meal == {}:
            return -6

        appetizer = self.find_dish(dish_id=meal_appetizer_id)
        main = self.find_dish(dish_id=meal_main_id)
        dessert = self.find_dish(dish_id=meal_dessert_id)

        if appetizer == {} or main == {} or dessert == {}:
            return -6

        self.meals[meal_id]["name"] = meal_name
        self.meals[meal_id]["appetizer"] = meal_appetizer_id
        self.meals[meal_id]["main"] = meal_main_id
        self.meals[meal_id]["dessert"] = meal_dessert_id

        self.meals[meal_id]["cal"], self.meals[meal_id]["sodium"], self.meals[meal_id][
            "sugar"] = self.__calculate_meal_nutrition(appetizer, main, dessert)

        return meal_id
