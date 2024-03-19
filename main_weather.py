from db_weather import Database
from methods_weather import WeatherMethods

if __name__ == "__main__":
    db = Database()
    api_key = "928e9e38a4e14bc0d4b3b0a01d766e93"

    weather_methods = WeatherMethods(db, api_key)
    current_user = None
    while True:
        print("\nWelcome to Weather App")
        print("1. Register")
        print("2. Login")
        print("3. Search weather by city")
        print("4. Search weather by coordinates")
        print("5. Display search history")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            weather_methods.register_user(username, password)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if weather_methods.login(username, password):
                current_user = username
            else:
                current_user = None

        elif choice == "3":
            if current_user:
                city_name = input("Enter city name: ")
                result = weather_methods.search_weather_by_city(city_name)
                if result:
                    weather_methods.save_search_history(current_user, city_name, result)
            else:
                print("Please login first!")

        elif choice == "4":
            if current_user:
                lat = input("Enter latitude: ")
                lon = input("Enter longitude: ")
                result = weather_methods.search_weather_by_coords(lat, lon)
                if result:
                    weather_methods.save_search_history(
                        current_user, f"({lat},{lon})", result
                    )
            else:
                print("Please login first!")

        elif choice == "5":
            if current_user:
                weather_methods.display_search_history(current_user)
            else:
                print("Please login first!")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")
