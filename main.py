import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QAction, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 600, 450)
        self.setFixedSize(600, 450)
        self.setupMenu()
        self.setupUI()
        self.applyStyles()

    def setupMenu(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
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
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_label = QLabel("Weather App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(title_label)
        
        input_layout = QHBoxLayout()
        self.city_label = QLabel("City:")
        self.city_label.setFont(QFont("Segoe UI", 12))
        self.city_input = QLineEdit()
        self.city_input.setFont(QFont("Segoe UI", 12))
        self.get_button = QPushButton("Get Weather")
        self.get_button.setFont(QFont("Segoe UI", 12))
        self.get_button.clicked.connect(self.get_weather)
        
        input_layout.addWidget(self.city_label)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.get_button)
        layout.addLayout(input_layout)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.output_text)

    def applyStyles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f5f7fa, stop:1 #c3cfe2);
            }
            QMenuBar {
                background-color: #2c3e50;
                color: white;
            }
            QMenuBar::item {
                padding: 6px 12px;
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
                color: #2c3e50;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)

    def showAbout(self):
        QMessageBox.about(self, "About Weather App",
                          "Weather App\nVersion 1.0\nPowered by OpenWeatherMap and Go.")

    def format_error_message(self, error_text):
        """Returns formatted HTML for error display."""
        return f"""
        <html>
        <head>
          <style>
            body {{
              font-family: "Segoe UI", sans-serif;
              background-color: #fff;
              margin: 0;
              padding: 10px;
            }}
            .error-container {{
              border: 1px solid #D8000C;
              background-color: #FFBABA;
              color: #D8000C;
              padding: 10px;
              border-radius: 5px;
            }}
            .error-header {{
              font-weight: bold;
              font-size: 16px;
              margin-bottom: 5px;
            }}
          </style>
        </head>
        <body>
          <div class="error-container">
            <div class="error-header">Error:</div>
            <div class="error-message">{error_text}</div>
          </div>
        </body>
        </html>
        """

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.output_text.setHtml(self.format_error_message("Please enter a city name."))
            return

        try:
            if not os.path.isfile("./weather") or not os.access("./weather", os.X_OK):
                self.output_text.setHtml(self.format_error_message("Error: The 'weather' binary is missing or not executable."))
                return

            result = subprocess.run(
                ["./weather", city],
                capture_output=True,
                text=True,
                check=True
            )
            weather_data = json.loads(result.stdout)
            formatted_text = (
                f"<div style='font-family: Segoe UI, sans-serif; color: #2c3e50;'>"
                f"<strong>City:</strong> {weather_data.get('name', 'N/A')}<br>"
                f"<strong>Temperature:</strong> {weather_data.get('main', {}).get('temp', 'N/A')} °C<br>"
                f"<strong>Humidity:</strong> {weather_data.get('main', {}).get('humidity', 'N/A')}%<br>"
                f"<strong>Wind Speed:</strong> {weather_data.get('wind', {}).get('speed', 'N/A')} m/s<br>"
            )
            weather_list = weather_data.get('weather', [])
            if weather_list and isinstance(weather_list, list):
                description = weather_list[0].get('description', 'N/A')
                formatted_text += f"<strong>Description:</strong> {description}<br>"
            formatted_text += "</div>"
            self.output_text.setHtml(formatted_text)
        except subprocess.CalledProcessError as e:
            self.output_text.setHtml(self.format_error_message(e.stderr.strip()))
        except json.JSONDecodeError:
            self.output_text.setHtml(self.format_error_message("Error: Unable to parse weather data.\n" + result.stdout.strip()))
        except Exception as ex:
            self.output_text.setHtml(self.format_error_message(f"An error occurred:\n{str(ex)}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())