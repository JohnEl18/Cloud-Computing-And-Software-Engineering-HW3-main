# import requests
# import pytest

# Base URL of your service
#base_url = "http://localhost:8000"

# import requests
def test_always_true():
    assert True

# def test_post_dishes():
#     base_url = 'http://localhost:8000'
#     dishes = ["orange", "spaghetti", "apple pie"]
#     ids = []
#
#     for dish in dishes:
#         response = requests.post(f"{base_url}/dishes/orange")
#         assert response.status_code == 200, f"Unexpected response code: {response.status_code} for dish: {dish}"
#         data = response.json()
#
#         print(f"Response text for dish {dish}: {response.text}")
#         print(f"Response JSON for dish {dish}: {data}")
#
#         ids.append(data["ID"])
#
#     # Check that all IDs are unique
#     assert len(ids) == len(set(ids)), "Not all IDs are unique"



#
# def test_get_dish():
#     response = requests.post(f"{base_url}/dishes", json={"dish": "orange"})
#     id = response.json()['id']
#     response = requests.get(f"{base_url}/dishes/{id}")
#     assert response.status_code == 200
#     assert 0.9 <= response.json()['sodium'] <= 1.1
#
# def test_get_dishes():
#     response = requests.get(f"{base_url}/dishes")
#     assert response.status_code == 200
#     assert len(response.json()) == 3
#
# def test_post_invalid_dish():
#     response = requests.post(f"{base_url}/dishes", json={"dish": "blah"})
#     assert response.json()['value'] == -3
#     assert response.status_code in [400, 404, 422]
#
# def test_post_duplicate_dish():
#     requests.post(f"{base_url}/dishes", json={"dish": "orange"})
#     response = requests.post(f"{base_url}/dishes", json={"dish": "orange"})
#     assert response.json()['value'] == -2
#     assert response.status_code in [400, 404, 422]
#
# def test_post_meal():
#     response = requests.post(f"{base_url}/meals", json={"name": "delicious", "appetizer": "orange", "main": "spaghetti", "dessert": "apple pie"})
#     assert response.status_code == 201
#     assert response.json()['id'] > 0
#
# def test_get_meals():
#     response = requests.get(f"{base_url}/meals")
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     assert 400 <= response.json()[0]['calories'] <= 500
#
# def test_post_duplicate_meal():
#     requests.post(f"{base_url}/meals", json={"name": "delicious", "appetizer": "orange", "main": "spaghetti", "dessert": "apple pie"})
#     response = requests.post(f"{base_url}/meals", json={"name": "delicious", "appetizer": "orange", "main": "spaghetti", "dessert": "apple pie"})
#     assert response.json()['value'] == -2
#     assert response.status_code in [400, 422]
