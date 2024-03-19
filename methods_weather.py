import hashlib
import requests


class WeatherMethods:
    def __init__(self, db, api_key):
        self.db = db
        self.api_key = api_key

    def register_user(self, username, password):
        password_hash = hashlib.sha512(password.encode()).hexdigest()
        self.db.cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        self.db.conn.commit()
        print("User registered successfully!")

    def login(self, username, password):
        password_hash = hashlib.sha512(password.encode()).hexdigest()
        self.db.cur.execute(
            "SELECT * FROM users WHERE username=? AND password_hash=?",
            (username, password_hash),
        )
        user = self.db.cur.fetchone()
        if user:
            print("Login successful!")
            return True
        else:
            print("Incorrect username or password!")
            return False

    def search_weather_by_city(self, city_name):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temperature_kelvin = data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            print(f"Weather in {city_name}: Temperature {temperature_celsius:.2f}°C")
            return temperature_celsius
        else:
            print("City not found or API request failed!")

    def search_weather_by_coords(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temperature_kelvin = data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            print(f"Weather at ({lat},{lon}): Temperature {temperature_celsius:.2f}°C")
            return temperature_celsius
        else:
            print("Weather not found for the provided coordinates!")

    def save_search_history(self, username, query, result):
        self.db.cur.execute(
            "INSERT INTO search_history (username, query, result) VALUES (?, ?, ?)",
            (username, query, result),
        )
        self.db.conn.commit()

    def display_search_history(self, username):
        self.db.cur.execute(
            "SELECT * FROM search_history WHERE username=?", (username,)
        )
        history = self.db.cur.fetchall()
        if history:
            print("Search History:")
            for row in history:
                print(f"Query: {row[2]}, Result: {row[3]}")
        else:
            print("No search history found!")
