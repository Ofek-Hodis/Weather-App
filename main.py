import sys
from weather import get_weather
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPushButton, QVBoxLayout, QLineEdit
from datetime import datetime, timezone, timedelta
from PyQt6.QtCore import Qt  # Imported to help with text alignement
from PyQt6.QtGui import QFont  # Imported for font styling


class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.search_button.clicked.connect(self.search_click)  # Indicating what function to run when button is pressed

    def settings(self):  # A method to define basic visual settings
        self.setWindowTitle("Weather-Search")
        self.setGeometry(300, 300, 600, 400)

    def initUI(self):
        self.title = QLabel("Weather-Search")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your city name")  # Text that will be displayed before searching

        self.output = QLabel("Weather PLACEHOLDER")
        self.search_button = QPushButton("Search")

        self.desgin = QVBoxLayout()  # This will be the main design setting
        self.desgin.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.desgin.addWidget(self.input_box)
        self.desgin.addWidget(self.output)
        self.desgin.addWidget(self.search_button)

        self.setLayout(self.desgin)  # Setting the layout to be based on the main design setting

        self.setStyleSheet("""
            QWidget {
            background-color: #ecf0d4;
            }

            QLabel {
            color: #3498db;
            }

            QLineEdit {
            background-color: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
            padding: 5px;
            }

            QLabel#output {
            color: #2c3e50;
            }

            QPushButton {
            background-color: #3498db;
            color: #ffffff;
            border: 1px solid #2980b9;
            padding: 10px;
            font-size: 28px;
            font-weight: bold;
            border-radius: 5px;
            }
        """)

    def search_click(self):
        self.results = self.search_weather(self.input_box.text())
        self.output.setText(self.results)

    def search_weather(self, city):
        weather_data = get_weather(city)
        if weather_data.status_code == 200:
            time_zone = weather_data.json()['timezone']  # The offset from UTC (Coordinated universal time) in seconds
            utc_now = datetime.now(timezone.utc)  # saving the current hour in UTC (Coordinated universal time)
            local_time = utc_now + timedelta(seconds=time_zone)
            local_hour = str(local_time.time())[:5]

            info = (f"{city.capitalize()}:\n"
                    f"{weather_data.json()['weather'][0]['main']}\n"
                    f"{weather_data.json()['main']['temp']} degrees Celsius\n"
                    f"Local time: {local_hour}\n"
                    f"Humidity: {weather_data.json()['main']['humidity']}%\n"
                    f"Wind speed: {weather_data.json()['wind']['speed']} kmph\n"
            )

            return info
        else:
            return f"Error: {weather_data.json()['message']}"

if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    main.show
    app.exec()
