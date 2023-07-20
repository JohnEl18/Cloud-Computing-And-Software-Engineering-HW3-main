import json

import requests

SERVICE_URL = "http://localhost:8000"
DISHES_ENDPOINT = "dishes"

INPUT_FILE_PATH = "query.txt"
OUTPUT_FILE_PATH = "response.txt"


def main():
    dishes = None

    with open(INPUT_FILE_PATH, "r") as input_file:
        with open(OUTPUT_FILE_PATH, "w") as output_file:
            for dish in input_file.readlines():
                dish = dish.replace('\n', '')
                add_dish_response = requests.post(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}",
                                                  headers={"Content-Type": "application/json"},
                                                  data=json.dumps({"name": dish}))

                dish_id = add_dish_response.text.replace('\n', '')
                get_dish_response = requests.get(url=f"{SERVICE_URL}/{DISHES_ENDPOINT}/{dish_id}")

                dish_nutrition = get_dish_response.json()

                output_line = f"{dish} contains {dish_nutrition['cal']} calories, {dish_nutrition['sodium']} mgs of sodium, and {dish_nutrition['sugar']} grams of sugar\n"


if __name__ == '__main__':
    main()
