import json

import requests

SERVICE_URL = "http://my-service-container:8000"
DISHES_ENDPOINT = "dishes"

ORANGE_DISH_ID = None


# import requests
def test_always_true():
    assert True


def test_add_three_dishes():
    dishes = ["orange", "spaghetti", "apple pie"]
    added_dishes_id = []

    for dish in dishes:
        response = requests.post(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps({"name": dish}))

        assert response.content in added_dishes_id
        assert response.status_code == 201

        if dish == "orange":
            ORANGE_DISH_ID = response.content
        added_dishes_id.append(response.content)


def test_retrieve_orange_dish():
    assert ORANGE_DISH_ID is not None

    response = requests.get(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}/{ORANGE_DISH_ID}")

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
    assert response.content == "-3"
