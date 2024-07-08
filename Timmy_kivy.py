from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.hunger = 50
        self.happiness = 50

    def feed(self):
        if self.hunger > 0:
            self.hunger -= 10
            if self.hunger < 0:
                self.hunger = 0
            return f"{self.name} has been fed."
        else:
            return f"{self.name} is not hungry."

    def play(self):
        self.happiness += 10
        if self.happiness > 100:
            self.happiness = 100
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        return f"You played with {self.name}."

    def show_status(self):
        return (f"{self.name}'s status:\n"
                f"  Age: {self.age} days\n"
                f"  Hunger: {self.hunger}\n"
                f"  Happiness: {self.happiness}")

    def age_pet(self):
        self.age += 1
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        self.happiness -= 5
        if self.happiness < 0:
            self.happiness = 0
        return f"\nA day has passed. {self.name} is now {self.age} days old."


class VirtualPetApp(App):
    def build(self):
        self.pet = None
        self.action_count = 0

        self.layout = BoxLayout(orientation='vertical')

        self.name_label = Label(text="Enter pet's name:")
        self.layout.add_widget(self.name_label)

        self.name_input = TextInput(multiline=False)
        self.layout.add_widget(self.name_input)

        self.start_button = Button(text="Start", on_press=self.start)
        self.layout.add_widget(self.start_button)

        self.feed_button = Button(text="Feed", on_press=self.feed, disabled=True)
        self.layout.add_widget(self.feed_button)

        self.play_button = Button(text="Play", on_press=self.play, disabled=True)
        self.layout.add_widget(self.play_button)

        self.status_button = Button(text="Check Status", on_press=self.show_status, disabled=True)
        self.layout.add_widget(self.status_button)

        self.quit_button = Button(text="Quit", on_press=self.stop)
        self.layout.add_widget(self.quit_button)

        self.status_label = Label(text="")
        self.layout.add_widget(self.status_label)

        return self.layout

    def start(self, instance):
        name = self.name_input.text
        if not name:
            popup = Popup(title='Input Error',
                          content=Label(text='Please enter a name for your pet.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        self.pet = VirtualPet(name)
        self.update_status(f"Welcome {self.pet.name}!")

        self.feed_button.disabled = False
        self.play_button.disabled = False
        self.status_button.disabled = False
        self.start_button.disabled = True

    def feed(self, instance):
        if not self.pet:
            return
        result = self.pet.feed()
        self.update_status(result)
        self.increment_action_count()

    def play(self, instance):
        if not self.pet:
            return
        result = self.pet.play()
        self.update_status(result)
        self.increment_action_count()

    def show_status(self, instance):
        if not self.pet:
            return
        status = self.pet.show_status()
        self.update_status(status)

    def update_status(self, message):
        self.status_label.text += f"{message}\n"

    def increment_action_count(self):
        self.action_count += 1
        if self.action_count >= 4:
            result = self.pet.age_pet()
            self.update_status(result)
            self.action_count = 0


if __name__ == "__main__":
    VirtualPetApp().run()
