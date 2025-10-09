import sys
from weather import get_weather
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPushButton, QVBoxLayout, QLineEdit
from datetime import datetime, timezone, timedelta


class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()

    def settings(self):  # A method to define basic visual settings
        self.setWindowTitle("Weather-Search")
        self.setGeometry(300, 300, 600, 400)

    def initUI(self):
        self.title = QLabel("Weather-Search")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your city name")  # Text that will be displayed before searching

        self.output = QLabel("Weather PLACEHOLDER")
        self.search_button = QPushButton("Search")

        self.desgin = QVBoxLayout()  # This will be the main desgin setting
        self.desgin.addWidget(self.title)
        self.desgin.addWidget(self.input_box)
        self.desgin.addWidget(self.output)
        self.desgin.addWidget(self.search_button)

        self.setLayout(self.desgin)  # Setting the layout to be based on the main design setting

    def search_click(self):
        pass

    def search_weather(self, city):
        weather_data = get_weather(city)
        if weather_data.status_code == 200:
            weather_description = weather_data.json()['weather'][0]['main']
            temp = weather_data.json()['main']['temp']
            humidity = weather_data.json()['main']['humidity']
            wind_speed = weather_data.json()['wind']['speed']

            time_zone = weather_data.json()['timezone']  # The offset from UTC (Coordinated universal time) in seconds
            utc_now = datetime.now(timezone.utc)  # saving the current hour in UTC (Coordinated universal time)
            local_time = utc_now + timedelta(seconds=time_zone)
            local_hour = str(local_time.time())[:8]

        elif weather_data.status_code == 404:
            pass

if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    main.show
    app.exec()
