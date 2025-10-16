import requests  # Imported to have contact with
from dotenv import load_dotenv  # Importing the function allowing to import data from a .env file
import os  # Allows Python to interact with the os, needed for the communication with the .env file
# Importing a command used to navigate to a specific file type (will be used to locate the .env file)
from pathlib import Path


def get_weather(city):
    # Loading the variables from the .env file by saving the path and giving it to the function load_dotenv()
    env_path = Path(__file__).resolve().parent / "API_key.env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("API_KEY")
    #  Opening the url of the relevant city using the input and the API key
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")
    return weather_data

