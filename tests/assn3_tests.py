import json

import requests

SERVICE_URL = "http://localhost:8000"
DISHES_ENDPOINT = "dishes"
MEALS_ENDPOINT = "meals"

ADDED_DISHES = {}


# import requests
def test_always_true():
    assert True


def test_add_three_dishes():
    dishes = ["orange", "spaghetti", "apple pie"]
    added_dishes_id = set()

    for dish in dishes:
        response = requests.post(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps({"name": dish}))

        assert response.status_code == 201

        ADDED_DISHES[dish] = response.content
        added_dishes_id.add(response.content)

    assert len(added_dishes_id) == 3

"""
def test_retrieve_orange_dish():
    assert "orange" in ADDED_DISHES.keys()

    response = requests.get(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}/{ADDED_DISHES['orange']}")

    assert response.status_code == 200
    nutrition = response.json()

    assert nutrition["sodium"] >= 0.9 and nutrition["sodium"] <= 1.1


def test_retrieve_all_dishes():
    response = requests.get(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}")

    assert response.status_code == 200

    dishes = response.json()
    assert len(dishes.keys()) == 3


def test_invalid_dish_name():
    response = requests.post(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps({"name": "blah"}))

    assert response.status_code in [404, 400, 422]
    assert int(response.content) == -3


def test_add_existing_dish():
    response = requests.post(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps({"name": "orange"}))

    assert response.status_code in [404, 400, 422]
    assert int(response.content) == -2


def test_add_meal():
    meal = {
        "name": "delicious",
        "appetizer": ADDED_DISHES["orange"],
        "main": ADDED_DISHES["spaghetti"],
        "dessert": ADDED_DISHES["apple pie"]
    }

    response = requests.post(url=f"{SERVICE_URL}/{MEALS_ENDPOINT}",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(meal))

    assert response.status_code == 201
    assert int(response.content) > 0


def test_retrieve_all_meals():
    response = requests.get(url=f"{SERVICE_URL}/{MEALS_ENDPOINT}")

    assert response.status_code == 200

    meals = response.json()
    assert len(meals.keys()) == 1

    assert meals[meals.keys()[0]]["cal"] >= 400 and meals[meals.keys()[0]]["cal"] <= 500


def test_add_existing_meal():
    meal = {
        "name": "delicious",
        "appetizer": ADDED_DISHES["orange"],
        "main": ADDED_DISHES["spaghetti"],
        "dessert": ADDED_DISHES["apple pie"]
    }

    response = requests.post(url=f"{SERVICE_URL}/{MEALS_ENDPOINT}",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(meal))

    assert response.status_code in [400, 422]
    assert response.content == "-2"

"""