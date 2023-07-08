def main():
    # Open your query.txt file
    with open("query.txt", 'r') as query_file:
        food_items = query_file.readlines()

    # Print the food items
    for food_item in food_items:
        print(food_item.strip())

if __name__ == "__main__":
    main()
