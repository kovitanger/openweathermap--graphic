import sys
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QAction, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 600, 400)
        self.setupMenu()
        self.setupUI()
        self.applyStyles()

    def setupMenu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

    def setupUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()
        self.get_button = QPushButton("Get Weather")
        self.get_button.clicked.connect(self.get_weather)

        input_layout.addWidget(self.city_label)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.get_button)
        layout.addLayout(input_layout)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        central_widget.setLayout(layout)

    def applyStyles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QMenuBar {
                background-color: #2c3e50;
                color: white;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            QMenu {
                background-color: #2c3e50;
                color: white;
            }
            QMenu::item:selected {
                background-color: #34495e;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)

    def showAbout(self):
        QMessageBox.about(self, "About Weather App",
                          "Weather App\nVersion 1.0\nPowered by OpenWeatherMap and Go.")

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.output_text.setPlainText("Please enter a city name.")
            return

        try:
            result = subprocess.run(
                ["./weather", city],
                capture_output=True,
                text=True,
                check=True
            )
            weather_data = json.loads(result.stdout)
            
            formatted_text = (
                f"City: {weather_data.get('name', 'N/A')}\n"
                f"Temperature: {weather_data.get('main', {}).get('temp', 'N/A')} °C\n"
                f"Humidity: {weather_data.get('main', {}).get('humidity', 'N/A')}%\n"
                f"Wind Speed: {weather_data.get('wind', {}).get('speed', 'N/A')} m/s\n"
            )
            
            weather_list = weather_data.get('weather', [])
            if weather_list and isinstance(weather_list, list):
                description = weather_list[0].get('description', 'N/A')
                formatted_text += f"Description: {description}\n"
            
            self.output_text.setPlainText(formatted_text)
        except subprocess.CalledProcessError as e:
            self.output_text.setPlainText(f"Error:\n{e.stderr}")
        except json.JSONDecodeError:
            self.output_text.setPlainText("Error: Unable to parse weather data.\n" + result.stdout)
        except Exception as ex:
            self.output_text.setPlainText(f"An error occurred:\n{str(ex)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
