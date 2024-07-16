import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os


# Class representing the virtual pet
class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.hunger = 50
        self.happiness = 50

    # Method to feed the pet
    def feed(self):
        if self.hunger > 0:
            self.hunger -= 10
            if self.hunger < 0:
                self.hunger = 0
            return f"{self.name} has been fed."
        else:
            return f"{self.name} is not hungry."

    # Method to play with the pet
    def play(self):
        self.happiness += 10
        if self.happiness > 100:
            self.happiness = 100
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        return f"You played with {self.name}."

    # Method to show the pet's status
    def show_status(self):
        return (f"{self.name}'s status:\n"
                f"  Age: {self.age} days\n"
                f"  Hunger: {self.hunger}\n"
                f"  Happiness: {self.happiness}")

    # Method to age the pet
    def age_pet(self):
        self.age += 1
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        self.happiness -= 5
        if self.happiness < 0:
            self.happiness = 0
        return f"\nA day has passed. {self.name} is now {self.age} days old."


# Main application class using PyQt6
class VirtualPetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.pet = None
        self.action_count = 0
        self.initUI()

    # Initialize the user interface
    def initUI(self):
        self.setWindowTitle('Virtual Pet')  # Set the window title
        self.setGeometry(100, 100, 300, 400)  # Set the window size and position

        self.layout = QVBoxLayout()  # Create the main layout

        self.name_label = QLabel("Enter pet's name:")  # Create a label for the pet's name
        self.layout.addWidget(self.name_label)  # Add the label to the layout

        self.name_input = QLineEdit(self)  # Create a text input for the pet's name
        self.layout.addWidget(self.name_input)  # Add the text input to the layout

        self.start_button = QPushButton('Start', self)  # Create the start button
        self.start_button.clicked.connect(self.start)  # Connect the start button to the start method
        self.layout.addWidget(self.start_button)  # Add the start button to the layout

        self.feed_button = QPushButton('Feed', self)  # Create the feed button
        self.feed_button.clicked.connect(self.feed)  # Connect the feed button to the feed method
        self.feed_button.setEnabled(False)  # Disable the feed button initially
        self.layout.addWidget(self.feed_button)  # Add the feed button to the layout

        self.play_button = QPushButton('Play', self)  # Create the play button
        self.play_button.clicked.connect(self.play)  # Connect the play button to the play method
        self.play_button.setEnabled(False)  # Disable the play button initially
        self.layout.addWidget(self.play_button)  # Add the play button to the layout

        self.status_button = QPushButton('Check Status', self)  # Create the status button
        self.status_button.clicked.connect(self.show_status)  # Connect the status button to the show_status method
        self.status_button.setEnabled(False)  # Disable the status button initially
        self.layout.addWidget(self.status_button)  # Add the status button to the layout

        self.quit_button = QPushButton('Quit', self)  # Create the quit button
        self.quit_button.clicked.connect(self.close)  # Connect the quit button to the close method
        self.layout.addWidget(self.quit_button)  # Add the quit button to the layout

        self.status_label = QLabel("", self)  # Create a label to display the status
        self.layout.addWidget(self.status_label)  # Add the status label to the layout

        self.image_label = QLabel(self)  # Create a label to display images
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image label
        self.layout.addWidget(self.image_label)  # Add the image label to the layout

        self.setLayout(self.layout)  # Set the main layout for the window

    # Method to start the virtual pet
    def start(self):
        name = self.name_input.text()  # Get the name from the text input
        if not name:
            QMessageBox.warning(self, 'Input Error',
                                'Please enter a name for your pet.')  # Show a warning if the name is empty
            return

        self.pet = VirtualPet(name)  # Create a new virtual pet
        self.update_status(f"Welcome {self.pet.name}!")  # Update the status

        self.feed_button.setEnabled(True)  # Enable the feed button
        self.play_button.setEnabled(True)  # Enable the play button
        self.status_button.setEnabled(True)  # Enable the status button
        self.start_button.setEnabled(False)  # Disable the start button

    # Method to feed the virtual pet
    def feed(self):
        if not self.pet:
            return
        result = self.pet.feed()  # Feed the pet
        self.update_status(result)  # Update the status
        self.increment_action_count()  # Increment the action count
        self.show_image('happy_cat.png')  # Show the feeding image

    # Method to play with the virtual pet
    def play(self):
        if not self.pet:
            return
        result = self.pet.play()  # Play with the pet
        self.update_status(result)  # Update the status
        self.increment_action_count()  # Increment the action count
        self.show_image('jumping_cat.png')  # Show the playing image

    # Method to show the virtual pet's status
    def show_status(self):
        if not self.pet:
            return
        status = self.pet.show_status()  # Get the pet's status
        self.update_status(status)  # Update the status

    # Method to update the status label
    def update_status(self, message):
        self.status_label.setText(message)  # Set the status label text

    # Method to increment the action count and age the pet if needed
    def increment_action_count(self):
        self.action_count += 1  # Increment the action count
        if self.action_count >= 4:
            result = self.pet.age_pet()  # Age the pet
            self.update_status(result)  # Update the status
            self.action_count = 0  # Reset the action count

    # Method to display an image
    def show_image(self, image_path):
        # Check if the image file exists
        if not os.path.exists(image_path):
            QMessageBox.warning(self, 'Image Error', f"Image {image_path} not found.")
            return
        pixmap = QPixmap(image_path)  # Load the image
        self.image_label.setPixmap(
            pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))  # Set the image in the label


# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    window = VirtualPetApp()  # Create the main window
    window.show()  # Show the main window
    sys.exit(app.exec())  # Run the application
