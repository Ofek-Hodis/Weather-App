import sys
import json

from PyQt6.QtWidgets import QTabWidget, QHBoxLayout

from weather import get_weather
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QInputDialog
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

        self.add_button.clicked.connect(self.add_click)
        self.add_box.returnPressed.connect(self.add_click)  # Also runs when pressing enter
        self.delete_button.clicked.connect(self.delete_click)


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
        self.fav_title = QLabel("Favorite Cities")
        self.add_box = QLineEdit()
        self.add_box.setPlaceholderText("Add to favorites...")  # Text that will be displayed before searching
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.action_description = QLabel("")
        self.info1 = QLabel("")
        self.info2 = QLabel("")
        self.info3 = QLabel("")

        favorites_layout = QVBoxLayout()  # This will be the main design setting
        favorites_layout.addWidget(self.fav_title, alignment=Qt.AlignmentFlag.AlignCenter)
        favorites_layout.addWidget(self.add_box)
        favorites_layout.addWidget(self.action_description)
        favorites_layout.addWidget(self.add_button)
        favorites_layout.addWidget(self.delete_button)

        info_row = QHBoxLayout()  # Lining up information in a row
        info_row.addWidget(self.info1)
        info_row.addWidget(self.info2)
        info_row.addWidget(self.info3)
        favorites_layout.addLayout(info_row)  # Adding the row to the layout

        self.favorites_tab.setLayout(favorites_layout)
        self.update_favs()

        # self.setStyleSheet("""""")

    def add_click(self):
        results = self.add_favs(self.add_box.text())
        self.action_description.setText(results)
        self.update_favs()

    def update_favs(self):
        with open("Data/favorites.JSON", "r") as f:
            data = json.load(f)

        if data[0] != "":
            info1 = self.search_weather(data[0])
            self.info1.setText(info1)
            if data[1] != "":
                info2 = self.search_weather(data[1])
                self.info2.setText(info2)
                if data[2] != "":
                    info3 = self.search_weather(data[2])
                    self.info3.setText(info3)
                else:
                    self.info3.setText("")
            else:
                self.info2.setText("")
        else:
            self.info1.setText("")


    def add_favs(self, city):
        weather_data = get_weather(city)
        if weather_data.status_code == 200:  # Verifying the city exists
            with open("Data/favorites.JSON", "r+") as f:
                data = json.load(f)
                place = -1  # Starting value for a variable to track first available space
                is_changed = False
                quantity = data[len(data) - 1]  # Last cell stores the current number of favorited cities
                if quantity < 3:  # Verifying the favorites cities quantity is below the limit
                    for i in range(0, len(data) - 1):  # Last cell in json list is the length of the list, avoiding it
                        if data[i] == city:
                            return "City is already in favorites."
                        if data[i] == "" and not is_changed:
                            place = i
                            is_changed = True
                    data[place] = city
                    data[len(data) - 1] = quantity + 1
                    with open("Data/favorites.JSON", "w") as f:
                        json.dump(data, f)
                    return f"{city.capitalize()} has been added to favorites"
                else:
                    return "Favorites full, please remove a city."
        else:
            return f"Error: {weather_data.json()['message']}"

    def search_click(self):
        results = self.search_weather(self.input_box.text())
        self.output.setText(results)

    def delete_click(self):
        with open("Data/favorites.JSON", "r") as f:
            data = json.load(f)
            fav_quantity = data.pop()  # Removing the last cell, used to keep list length
            if fav_quantity == 0:
                return
            data = [x for x in data if x != ""]  # Removing empty cells from the list
            # 0 indicates index of default choice, False indicates that user can't type in answer
            item, ok = QInputDialog.getItem(self, "Remove city", "Choose a city:", data, 0, False)
            if ok and item:
                self.delete_city(item)

    def delete_city(self, city):
        with open("Data/favorites.JSON", "r+") as f:
            data = json.load(f)
            data = ["" if x == city else x for x in data]  # Changing the cell of the deleted city to be empty
            data[-1] = data[-1] - 1  # Updating the cell that holds the length
        for i in range(0, len(data)-2):  # Shuffling through the list to place the empty cells at the end
            if data[i] == "":
                next_cell = data[i + 1]
                data[i] = next_cell
                data[i + 1] = ""

        with open("Data/favorites.JSON", "w") as f:  # Removing previous list and dumping updated version
           json.dump(data, f)
        self.action_description.setText(f"{city.capitalize()} has been removed from favorites")
        self.update_favs()  # Updating the favorites display

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
