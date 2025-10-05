import requests  # Imported to have contact with
from datetime import datetime, timezone, timedelta

api_key = '687537ea02a6941b4b5c348c3c6488be'
user_input = input("Choose a city: ")
#  Opening the url of the relevant city using the input and the API key
weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")

if weather_data.json()['cod'] == '404':  # Checking the city was found
    print("Error: City not found")
else:
    weather = weather_data.json()['weather'][0]['main']
    temp = weather_data.json()['main']['temp']
    time_zone = weather_data.json()['timezone']  # The offset from UTC (Coordinated universal time) in seconds
    utc_now = datetime.now(timezone.utc)  # saving the current hour in UTC (Coordinated universal time)
    local_time = utc_now + timedelta(seconds=time_zone)
    local_hour = str(local_time.time())[:8]

    print(f"The weather in {user_input} is {weather}, {temp} degrees Celsius")
    print(f"The local time is {local_hour}")
