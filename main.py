import sys

from PyQt6.QtWidgets import QTabWidget

from weather import get_weather
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPushButton, QVBoxLayout, QLineEdit
from datetime import datetime, timezone, timedelta
from PyQt6.QtCore import Qt  # Imported to help with text alignment
from PyQt6.QtGui import QFont  # Imported for font styling


class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()

        # Handling tab creation
        self.tabs = QTabWidget()
        self.weather_tab = QWidget()
        self.favorites_tab = QWidget()
        self.tabs.addTab(self.weather_tab, "Weather")
        self.tabs.addTab(self.favorites_tab, "Favorites")
        self.tabs.setCurrentWidget(self.weather_tab)  # Setting the weather tab to be loaded

        main_layout = QVBoxLayout()  # Creating a layout to display the tabs
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.style_tabs()
        self.init_weather_UI()
        self.init_favorites_UI()
        self.search_button.clicked.connect(self.search_click)  # Indicating what function to run when button is pressed
        self.input_box.returnPressed.connect(self.search_click)  # Also runs when pressing enter

    def settings(self):  # A method to define basic visual settings
        self.setWindowTitle("Weather-Search")
        #self.setWindowIcon()
        self.setGeometry(300, 300, 600, 400)

    def init_weather_UI(self):
        self.title = QLabel("Weather-Search")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your city name")  # Text that will be displayed before searching

        self.output = QLabel("Enter your city into the search box to get weather information!")
        self.output.setObjectName('output')
        self.search_button = QPushButton("Search")

        weather_layout = QVBoxLayout()  # This will be the main design setting
        weather_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        weather_layout.addWidget(self.input_box)
        weather_layout.addWidget(self.output)
        weather_layout.addWidget(self.search_button)

        self.weather_tab.setLayout(weather_layout)  # Setting the layout to be based on the main design setting

        self.setStyleSheet("""
            QWidget {
            background-color: #ecf0d4;
            }

            QLabel {
            color: #3498db;
            padding: 7px;
            font-size: 20px;
            font-weight: bold;
            }

            QLineEdit {
            background-color: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
            padding: 5px;
            }

            QLabel#output {
            color: #2c3e50;
            font-size: 14px;
            }

            QPushButton {
            background-color: #3498db;
            color: #ffffff;
            border: 1px solid #2980b9;
            padding: 7px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
            }
        """)

    def style_tabs(self):
        # Accessing the tab bar of the tabs widget to style it
        self.tabs.tabBar().setStyleSheet('''
        QTabBar::tab:selected {
        background-color:#d0d4b8;
        color: white;
        font-weight: bold;
        font-size: 12px;
        }
        QTabBar::tab:!selected:hover {
        background-color:#d0d4b8;
        color: gray;
        font-weight: bold;
        font-size: 12px;
        }
        QTabBar::tab:!selected {
        background-color:#d0d4b8;
        color: black;
        font-weight: bold;
        font-size: 12px;
        }
        
        ''')

    def init_favorites_UI(self):
        pass

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
