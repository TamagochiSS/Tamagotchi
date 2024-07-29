import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  ### Goda 28.07.2024: Added ImageTk for displaying images
import time
import json  # Lib for the JSON file format
import os  # Library to help with the save utility
import random
import customtkinter as ctk
import subprocess  # starts new process to open other file

SAVE_FILE = "pets_data.json"

ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")


class VirtualPet:
    '''
    VirtualPet class, holding all functions to change the pets properties/statistics
    '''

    def __init__(self, name, age=0, hunger=50, happiness=50, health=50, tiredness=20, intellect=0):
        ''' Constructor to initialize a VirtualPet instance, used with default parameters as all pets are supposed
        to start with the same preconditions.
        '''
        self.name = name
        self.age = age  # In pet days
        self.hunger = hunger
        self.happiness = happiness
        self.health = health
        self.tiredness = tiredness
        self.intellect = intellect

    def feed(self, food_type):  # Janne
        '''
        feed VirtualPet and change scores according to food choice
        '''
        if food_type == "pizza":
            self.hunger = max(0, self.hunger - 20)
            self.health = max(0, self.health - 10)
            self.happiness = min(100, self.happiness + 5)
            self.tiredness = min(100, self.tiredness + 5)
        elif food_type == "salad":
            self.hunger = max(0, self.hunger - 15)
            self.health = min(100, self.health + 5)
            self.tiredness = max(0, self.tiredness - 5)
        elif food_type == "barbecue":
            self.hunger = max(0, self.hunger - 15)
            self.happiness = min(100, self.happiness + 10)
            self.tiredness = min(100, self.tiredness + 5)

        return f"You ate {food_type} with {self.name}."

    def play(self, game_type):  # Janne
        '''
        play with VirtualPet. pet statistics change depending on game_type
        '''
        if game_type == "hide and seek":
            self.happiness = min(100, self.happiness + 20)  # score does not exceed a value of 100
            self.hunger = min(100, self.hunger + 10)
            self.tiredness = min(100, self.tiredness + 5)
            self.hide_and_seek_game()
        elif game_type == "memory":
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 5)
            self.intellect = min(100, self.intellect + 10)
            self.memory_game()
        elif game_type == "beachball":
            self.happiness = min(100, self.happiness + 10)
            self.health = min(100, self.health + 5)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
            self.ball_game()

        # Call the random_event function after playing to print random event to console
        event_played = self.random_event()

        return f"You played {game_type} with {self.name}. {event_played}"

    # Create memory game - separate file memory_game.py / Janne
    def memory_game(self):
        '''
        starting memory game in a separate process
        '''
        subprocess.Popen(["python", "memory_game.py"])

    # Create hide and seek game - separate file hide_and_seek.py / Janne
    def hide_and_seek_game(self):
        '''
        starting hide and seek game in a separate process
        '''
        subprocess.Popen(["python", "hide_and_seek.py"])

    # Create beachball game - separate file ball_game.py / Janne
    def ball_game(self):
        '''
        starting hide and seek game in a separate process
        '''
        subprocess.Popen(["python", "ball_game.py"])

    def random_event(self):  # Janne
        '''
        when VirtualPet plays, a random event is caused, which changes both the scores and prints the event to the console
        '''
        events = ["saw a seldom bird", "stumbled and got hurt", "nothing happened"]
        event = random.choice(events)
        if event == "saw a seldom bird":
            self.happiness = min(100, self.happiness + 10)
            self.intellect = min(100, self.intellect + 5)
            return f"{self.name} saw a seldom bird and feels super happy!"
        elif event == "stumbled and got hurt":
            self.health = max(0, self.health - 10)  # score does not fall below a value of 0
            self.intellect = max(0, self.intellect - 10)
            return f"{self.name} lost balance and fell during playing. You should get a plaster and some sweets."
        elif event == "nothing happened":
            return f"{self.name} is very calm today."

    def TV(self):  # Janne
        '''
        when VirtualPet watches TV, a random show gets picked from the dictonary and the scores are adjusted accordingly. The show is printed in the console
        '''
        tv_show = [
            {"title": "cartoon", "happiness": 10, "hunger": 10, "tiredness": 5, "intellect": -10, "health": -5,
             "message": "It is so funny and entertaining!"},
            {"title": "documentary", "happiness": 10, "hunger": 5, "tiredness": 5, "intellect": 10, "health": -5,
             "message": "Exciting facts on nature are revealed!"},
            {"title": "a home workout channel", "happiness": 10, "hunger": 5, "tiredness": 15, "intellect": 5,
             "health": 10, "message": "Quite hard to keep up with the pace!"}
        ]

        show = random.choice(tv_show)
        self.happiness = min(100, self.happiness + show["happiness"])
        self.hunger = min(100, self.hunger + show["hunger"])
        self.tiredness = min(100, self.tiredness + show["tiredness"])
        self.intellect = min(100, max(0, self.intellect + show[
            "intellect"]))  # making sure that the score does not exceed 100 and does not fall below 0
        self.health = min(100, max(0, self.health + show["health"]))
        return f"{self.name} is watching {show['title']}. {show['message']}"

    def vet(self):
        '''
        send VirtualPet to the vet, improve health, decreases happiness points
        '''
        self.health = min(100, self.health + 20)
        self.happiness = max(0, self.happiness - 10)
        return f"{self.name} visited the vet."

    def sleep(self):
        '''
        send VirtualPet to sleep. Reduces happiness and tiredness, but improves health.
        '''
        self.tiredness = max(0, self.tiredness - 40)
        self.health = min(100, self.health + 10)
        self.happiness = max(0, self.happiness - 10)
        return f"{self.name} had a good sleep."

    def show_status(self):
        '''
        retrieve the current status of your pet
        '''
        return (f"{self.name}'s status:\n"
                f"  Age: {self.age} days\n"
                f"  Hunger: {self.hunger}\n"
                f"  Happiness: {self.happiness}\n"
                f"  Health: {self.health}\n"
                f"  Tiredness: {self.tiredness}\n"
                f"  Intellect: {self.intellect}")

    def to_dict(self, real_time_elapsed, pet_time_elapsed):
        '''
        returns a dictionary containing all pet data.
        '''
        return {
            'name': self.name,
            'age': self.age,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'tiredness': self.tiredness,
            'health': self.health,
            'intellect': self.intellect,
            'real_time_elapsed': real_time_elapsed,
            'pet_time_elapsed': pet_time_elapsed,
            'selected_animal': self.selected_animal  # Judit – 25.07.2024: Save the selected animal
        }

    @staticmethod
    def from_dict(data):
        pet = VirtualPet(data['name'], data['age'], data['hunger'], data['happiness'], data['tiredness'],
                         data['health'], data['intellect'])
        pet.selected_animal = data.get('selected_animal', 'cat')  # Judit – 25.07.2024: Default to 'cat' if not found
        return pet


################################################################################################################

class VirtualPetApp:
    '''
    class VirtualPetApp is used to visualize the VirtualPet and allows the user to change the pet scores by using
    different "buttons"
    '''

    def __init__(self, root):
        '''
        Initialize the VirtualPetApp
        '''
        self.root = root
        self.root.title("Virtual Pet")
        self.pet = None
        self.start_time = None  # Real start time
        self.real_seconds_elapsed = 0
        self.pet_seconds_elapsed = 0  # Pet time in seconds
        self.load_images()  # Judit – 25.07.2024: Load and scale images once
        self.create_widgets()
        self.load_pet_prompt()  # Check for saved pet data

    def load_images(self):  # Judit – 25.07.2024: Load and scale images once
        '''
    	load and scale images once
        '''
        self.animal_options = ["cat", "chicken", "shrimp", "sheep"]
        self.animal_images = {}
        for animal in self.animal_options:
            image_path = os.path.join('pet_pictures', f'picture_{animal}.png')  # Adjusted path to the images folder
            if not os.path.exists(image_path):
                continue
            image = Image.open(image_path)
            resized_image = image.resize((100, 100), Image.LANCZOS)  # Resize the image to a smaller format
            self.animal_images[animal] = ctk.CTkImage(light_image=resized_image, dark_image=resized_image,
                                                      size=(100, 100))  # Judit – 27.02.2024: Convert to CTkImage

        # Load button images
        self.play_image = ctk.CTkImage(
            light_image=Image.open('buttons/play_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/play_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.feed_image = ctk.CTkImage(
            light_image=Image.open('buttons/feed_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/feed_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.TV_image = ctk.CTkImage(light_image=Image.open('buttons/tv_button.png').resize((100, 100), Image.LANCZOS),
                                     dark_image=Image.open('buttons/tv_button.png').resize((100, 100), Image.LANCZOS),
                                     size=(100, 100))  # Judit – 27.02.2024
        self.sleep_image = ctk.CTkImage(
            light_image=Image.open('buttons/sleep_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/sleep_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.vet_image = ctk.CTkImage(
            light_image=Image.open('buttons/vet_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/vet_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024

        # Load new button images
        self.start_image = ctk.CTkImage(
            light_image=Image.open('buttons/start_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/start_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.load_image = ctk.CTkImage(
            light_image=Image.open('buttons/load_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/load_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.save_image = ctk.CTkImage(
            light_image=Image.open('buttons/save_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/save_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.check_status_image = ctk.CTkImage(
            light_image=Image.open('buttons/check_status_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/check_status_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024
        self.quit_image = ctk.CTkImage(
            light_image=Image.open('buttons/quit_button.png').resize((100, 100), Image.LANCZOS),
            dark_image=Image.open('buttons/quit_button.png').resize((100, 100), Image.LANCZOS),
            size=(100, 100))  # Judit – 27.02.2024

    def start(self):
        '''
        '''
        name = self.name_entry.get()
        self.pet = VirtualPet(name)
        # Enable the buttons when the start button is pressed
        self.save_button.configure(state="normal")
        self.feed_button.configure(state="normal")
        self.play_button.configure(state="normal")
        self.TV_button.configure(state="normal")
        self.sleep_button.configure(state="normal")
        self.vet_button.configure(state="normal")
        self.status_button.configure(state="normal")
        self.quit_button.configure(state="normal")

    def create_widgets(self):
        '''
        create all buttons and widgets used on the 4 different frames.
        top_frame shows pet name
        middle_frame holds all buttons and can be changed by using the change_middle_frame_to functions
        bottom_frame shows a console
        time frame shows the current time/age of pet.
        '''

        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(pady=10)

        self.middle_frame = ctk.CTkFrame(self.root)
        self.middle_frame.pack(pady=10)

        self.middle_frame_top = ctk.CTkFrame(self.middle_frame)  # Judit – 27.02.2024: New top frame for middle frame
        self.middle_frame_top.pack(pady=5)

        self.middle_frame_bottom = ctk.CTkFrame(
            self.middle_frame)  # Judit – 27.02.2024: New bottom frame for middle frame
        self.middle_frame_bottom.pack(pady=5)

        self.bottom_frame = ctk.CTkFrame(self.root)
        self.bottom_frame.pack(pady=10)

        self.time_frame = ctk.CTkFrame(self.root)
        self.time_frame.pack(pady=10)

        # Top Frame Widgets
        self.name_label = ctk.CTkLabel(self.top_frame, text="Enter pet's name:")
        self.name_label.pack(side="left", padx=5)

        self.name_entry = ctk.CTkEntry(self.top_frame)
        self.name_entry.pack(side="left", padx=5)
        # Middle Frame Widgets
        self.start_button = ctk.CTkButton(self.middle_frame_top, text="", image=self.start_image, compound="top",
                                          command=self.start)  # Judit – 27.02.2024: Removed text, added image
        self.start_button.pack(side="left", padx=5)

        self.load_button = ctk.CTkButton(self.middle_frame_top, text="", image=self.load_image, compound="top",
                                         command=self.load_pet_prompt)  # Judit – 27.02.2024: Removed text, added image
        self.load_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(self.middle_frame_top, text="", image=self.save_image, compound="top",
                                         command=self.save_pet,
                                         state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.save_button.pack(side="left", padx=5)

        self.feed_button = ctk.CTkButton(self.middle_frame_top, text="", image=self.feed_image, compound="top",
                                         command=self.show_feed_buttons, state="disabled")  # Janne
        self.feed_button.pack(side="left", padx=5)

        self.feed_pizza_button = ctk.CTkButton(self.middle_frame_bottom, text="Eat pizza",
                                               command=lambda: self.feed("pizza"))  # Janne
        self.feed_salad_button = ctk.CTkButton(self.middle_frame_bottom, text="Eat salad",
                                               command=lambda: self.feed("salad"))
        self.feed_barbecue_button = ctk.CTkButton(self.middle_frame_bottom, text="Have a barbecue",
                                                  command=lambda: self.feed("barbecue"))
        self.stop_eating_button = ctk.CTkButton(self.middle_frame_bottom, text="Finish eating",
                                                command=self.remove_feed_buttons)

        self.play_button = ctk.CTkButton(self.middle_frame_top, text="", image=self.play_image, compound="top",
                                         command=self.show_play_buttons,
                                         state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.play_button.pack(side="left", padx=5)

        self.play_hideandseek_button = ctk.CTkButton(self.middle_frame_bottom, text="Play hide and seek",
                                                     command=lambda: self.play(
                                                         "hide and seek"))  # Judit – 27.07.2024: Moved to middle_frame_bottom
        self.play_memory_button = ctk.CTkButton(self.middle_frame_bottom, text="Play memory", command=lambda: self.play(
            "memory"))  # Judit – 27.07.2024: Moved to middle_frame_bottom
        self.play_beachball_button = ctk.CTkButton(self.middle_frame_bottom, text="Play beachball",
                                                   command=lambda: self.play(
                                                       "beachball"))  # Judit – 27.07.2024: Moved to middle_frame_bottom
        self.stop_playing_button = ctk.CTkButton(self.middle_frame_bottom, text="Stop Playing",
                                                 command=self.remove_play_buttons)  # Judit – 27.07.2024: Moved to middle_frame_bottom

        self.TV_button = ctk.CTkButton(self.middle_frame_bottom, text="", image=self.TV_image, compound="top",
                                       command=self.TV,
                                       state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.TV_button.pack(side="left", padx=5)

        self.sleep_button = ctk.CTkButton(self.middle_frame_bottom, text="", image=self.sleep_image, compound="top",
                                          command=self.sleep,
                                          state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.sleep_button.pack(side="left", padx=5)

        self.vet_button = ctk.CTkButton(self.middle_frame_bottom, text="", image=self.vet_image, compound="top",
                                        command=self.vet,
                                        state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.vet_button.pack(side="left", padx=5)

        self.status_button = ctk.CTkButton(self.middle_frame_bottom, text="", image=self.check_status_image,
                                           compound="top", command=self.show_status,
                                           state="disabled")  # Judit – 27.02.2024: Removed text, added image
        self.status_button.pack(side="left", padx=5)

        self.quit_button = ctk.CTkButton(self.middle_frame_bottom, text="", image=self.quit_image, compound="top",
                                         command=self.root.destroy,
                                         state="normal")  ### Goda 28.07.2024: Changed to self.root.destroy to properly exit the application
        self.quit_button.pack(side="left", padx=5)

        # Bottom Frame Widgets
        self.status_text = ctk.CTkTextbox(self.bottom_frame, height=140, width=550)
        self.status_text.pack(side="left", padx=5)

        # Time Frame Widgets
        self.real_time_label = ctk.CTkLabel(self.time_frame, text="Real Time: 0s", text_color="darkgreen")
        self.real_time_label.pack(side="left", padx=10)

        self.pet_time_label = ctk.CTkLabel(self.time_frame, text="Pet Time: 0 pet days", text_color="darkgreen")
        self.pet_time_label.pack(side="left", padx=10)

        self.pet_image_label = ctk.CTkLabel(self.root)
        self.pet_image_label.pack()  # To display the selected pet's image after naming

    def show_play_buttons(self):
        '''
        function to display play buttons to choose from different play activities.
        '''
        self.play_hideandseek_button.pack(side="left", padx=5)  # Judit – 27.07.2024: Changed to pack side by side
        self.play_memory_button.pack(side="left", padx=5)  # Judit – 27.07.2024: Changed to pack side by side
        self.play_beachball_button.pack(side="left", padx=5)  # Judit – 27.07.2024: Changed to pack side by side
        self.stop_playing_button.pack(side="left", padx=5)  # Judit – 27.07.2024: Changed to pack side by side

    def remove_play_buttons(self):
        '''
        function called when "stop playing" button is clicked, removes the buttons for the mini games
        '''
        self.play_hideandseek_button.pack_forget()
        self.play_memory_button.pack_forget()
        self.play_beachball_button.pack_forget()
        self.stop_playing_button.pack_forget()

    def show_feed_buttons(self):  # Janne
        '''
        function to display food choice buttons
        '''
        self.feed_pizza_button.pack(side="left", padx=5)
        self.feed_salad_button.pack(side="left", padx=5)
        self.feed_barbecue_button.pack(side="left", padx=5)
        self.stop_eating_button.pack(side="left", padx=5)

    def remove_feed_buttons(self):  # Janne
        '''
        function called when "stop eating" button is clicked, removes the buttons for the food choices
        '''
        self.feed_pizza_button.pack_forget()
        self.feed_salad_button.pack_forget()
        self.feed_barbecue_button.pack_forget()
        self.stop_eating_button.pack_forget()

    def start(self):
        '''
        '''
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name for your pet.")
            return

        self.pet = VirtualPet(name)
        self.pet.selected_animal = self.selected_animal  # Judit – 25.07.2024: Save the selected animal
        self.start_time = time.time()  # Set the start time
        self.real_seconds_elapsed = 0  # Initialize real time elapsed
        self.pet_seconds_elapsed = 0  # Initialize pet time elapsed
        self.update_status(f"Welcome {self.pet.name}!")
        self.pet_image_label.configure(image=self.animal_images[self.selected_animal])  # Display selected pet's image
        self.save_button.configure(state=tk.NORMAL)
        self.feed_button.configure(state=tk.NORMAL)
        self.feed_pizza_button.configure(state=tk.NORMAL)
        self.feed_salad_button.configure(state=tk.NORMAL)
        self.feed_barbecue_button.configure(state=tk.NORMAL)
        self.play_button.configure(state=tk.NORMAL)
        self.TV_button.configure(state=tk.NORMAL)
        self.play_hideandseek_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
        self.play_memory_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
        self.play_beachball_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
        self.sleep_button.configure(state=tk.NORMAL)
        self.vet_button.configure(state=tk.NORMAL)
        self.status_button.configure(state=tk.NORMAL)
        self.quit_button.configure(state=tk.NORMAL)
        self.start_button.configure(state=tk.DISABLED)
        self.load_button.configure(state=tk.DISABLED)
        self.name_entry.configure(state=tk.DISABLED)

        self.update_times()
        self.update_pet_time()

    def pet_not_found(self):  # Judit – 25.07.2024: Handle pet not found scenario
        '''
        handles pet not found scenario
        '''
        messagebox.showinfo("Info", "Pet not found. Please select a new pet.")
        self.create_animal_selection_widgets()

    def create_animal_selection_widgets(self):
        # Judit – 25.07.2024: Animal selection
        '''
        choose an animal
        '''
        self.animal_label = ctk.CTkLabel(self.root, text="Wähle ein Tier:")
        self.animal_label.pack()

        self.animal_buttons = {}
        button_frame = ctk.CTkFrame(self.root)  # Create a frame to hold the buttons
        button_frame.pack()

        for animal in self.animal_options:
            self.animal_buttons[animal] = ctk.CTkButton(button_frame, image=self.animal_images[animal],
                                                        command=lambda a=animal: self.select_animal(a),
                                                        text="")  # Judit – 27.02.2024: Removed text
            self.animal_buttons[animal].pack(side=tk.LEFT, padx=10, pady=10)  # Add padding for spacing

    def select_animal(self, animal):
        '''

        '''
        self.selected_animal = animal

        for button in self.animal_buttons.values():
            button.pack_forget()
        self.animal_label.pack_forget()

        self.create_name_widgets()

    def create_name_widgets(self):
        '''
        '''
        self.name_label.pack()
        self.name_entry.pack()
        self.start_button.pack()

    def load_pet_prompt(self):  # Definition used for loading prompt when game starts
        '''
        '''
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file:  # Read mode
                pets_data = json.load(file)
            pet_names = list(pets_data.keys())
            if pet_names:
                pet_name = simpledialog.askstring("Load Pet", "Enter the name of the pet to load:",
                                                  initialvalue=pet_names[0])
                if pet_name and pet_name in pet_names:
                    self.load_pet(pet_name)
                else:
                    self.pet_not_found()  # Judit – 25.07.2024: Trigger the pet not found process
            else:
                messagebox.showinfo("Info", "No saved pets available.")
        else:
            self.pet_not_found()  # Judit – 27.02.2024: Trigger the pet not found process if save file doesn't exist

    def load_pet(self, pet_name):  # Logic for loading old pet.
        '''
        '''
        try:
            with open(SAVE_FILE, "r") as file:  # reads saved file
                pets_data = json.load(file)
                if pet_name in pets_data:
                    pet_data = pets_data[pet_name]
                    self.pet = VirtualPet.from_dict(pet_data)
                    self.real_seconds_elapsed = pet_data['real_time_elapsed']
                    self.pet_seconds_elapsed = pet_data['pet_time_elapsed']
                    self.start_time = time.time() - self.real_seconds_elapsed
                    self.selected_animal = pet_data.get('selected_animal',
                                                        'cat')  # Judit – 25.07.2024: Default to 'cat' if not found
                    self.update_status(f"Welcome back {self.pet.name}!")  # Welcome message
                    self.pet_image_label.configure(
                        image=self.animal_images[self.selected_animal])  # Display the selected pet's image
                    self.save_button.configure(state=tk.NORMAL)
                    self.feed_button.configure(state=tk.NORMAL)
                    self.play_button.configure(state=tk.NORMAL)
                    self.feed_pizza_button.configure(state=tk.NORMAL)
                    self.feed_salad_button.configure(state=tk.NORMAL)
                    self.feed_barbecue_button.configure(state=tk.NORMAL)
                    self.TV_button.configure(state=tk.NORMAL)
                    self.play_hideandseek_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
                    self.play_memory_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
                    self.play_beachball_button.configure(state=tk.NORMAL)  # Judit – 27.07.2024: Enable play buttons
                    self.sleep_button.configure(state=tk.NORMAL)
                    self.vet_button.configure(state=tk.NORMAL)
                    self.status_button.configure(state=tk.NORMAL)
                    self.quit_button.configure(state=tk.NORMAL)
                    self.start_button.configure(state=tk.DISABLED)
                    self.load_button.configure(state=tk.DISABLED)
                    self.name_entry.configure(state=tk.DISABLED)

                    self.update_times()
                    self.update_pet_time()
                else:
                    messagebox.showerror("Error", "Pet not found in the save file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pet: {e}")

    def save_pet(self):  # Definition used to save current playing pet
        '''
        '''
        if not self.pet:
            return
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as file:
                    pets_data = json.load(file)
            else:
                pets_data = {}

            pets_data[self.pet.name] = self.pet.to_dict(self.real_seconds_elapsed, self.pet_seconds_elapsed)

            with open(SAVE_FILE, "w") as file:  # Sets Write mode
                json.dump(pets_data, file, indent=4)

            self.update_status(f"{self.pet.name}'s data has been saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save pet: {e}")

    def update_times(self):
        '''
        '''
        if self.pet:
            # Real time elapsed since start
            current_time = time.time()
            real_time_elapsed = current_time - self.start_time
            self.real_seconds_elapsed = int(real_time_elapsed)
            self.real_time_label.configure(text=f"Real Time: {self.format_real_time(self.real_seconds_elapsed)}")

        # Schedule the update_times method to run again after 1000ms (1s)
        self.root.after(1000, self.update_times)

    def update_pet_time(self):
        '''
        '''
        if self.pet:
            # Update pet time independently
            self.pet_seconds_elapsed += 3600 / 24  # Increment pet time by 1 pet hour (3600 pet seconds)
            pet_days_elapsed = self.pet_seconds_elapsed / (24 * 60 * 60)
            old_age = self.pet.age
            self.pet.age = int(pet_days_elapsed)  # Update pet age in pet days
            if self.pet.age > old_age:
                self.update_status(f"A new pet day has passed. {self.pet.name} is now {self.pet.age} pet days old.")

            self.pet_time_label.configure(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

        # Schedule the update_pet_time method to run again after 1s
        self.root.after(1000, self.update_pet_time)

    def format_real_time(self, seconds):
        '''
        '''
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def format_pet_time(self, pet_seconds):
        '''
        '''
        pet_hours, pet_seconds = divmod(pet_seconds, 3600)
        pet_days, pet_hours = divmod(pet_hours, 24)
        pet_minutes, pet_seconds = divmod(pet_seconds, 60)
        return f"{int(pet_days)} pet days {int(pet_hours)}h {int(pet_minutes)}m {int(pet_seconds)}s"

    def feed(self, food_type):
        '''
        action caused by clicking feed-button. Calls feed function of pet.
        '''
        if not self.pet:
            return
        result = self.pet.feed(food_type)
        self.update_status(result)
        self.show_image("feed.png")  ### Goda 28.07.2024: Display image after feeding
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def play(self, game_type):
        '''
        Action caused by clicking play-button. Calls play function of pet.
        '''
        if not self.pet:
            return
        result = self.pet.play(game_type)
        self.update_status(result)
        self.show_image("play.png")  ### Goda 28.07.2024: Display image after playing
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def TV(self):
        '''
        Action causes by clicking TV-button.
        '''
        if not self.pet:
            return
        result = self.pet.TV()
        self.update_status(result)
        self.show_image("tv.png")  ### Goda 28.07.2024: Display image after watching TV
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def sleep(self):
        '''
        Action caused by clicking sleep button. Calls sleep function of VirtualPet.
        '''
        if not self.pet:
            return
        result = self.pet.sleep()
        self.update_status(result)
        self.show_image("sleep.png")  ### Goda 28.07.2024: Display image after sleeping
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def vet(self):
        '''
        Action caused by vet button. Calls vet function of VirtualPet.
        '''
        if not self.pet:
            return
        result = self.pet.vet()
        self.update_status(result)
        self.show_image("vet.png")  ### Goda 28.07.2024: Display image after visiting the vet
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def advance_pet_time(self, seconds):
        '''

        '''
        self.pet_seconds_elapsed += seconds  # Advance pet time by given seconds
        pet_days_elapsed = self.pet_seconds_elapsed / (24 * 60 * 60)
        old_age = self.pet.age
        self.pet.age = int(pet_days_elapsed)  # Update pet age in pet days
        if self.pet.age > old_age:
            self.update_status(f"A new pet day has passed. {self.pet.name} is now {self.pet.age} pet days old.")
        self.pet_time_label.configure(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

    def show_status(self):
        '''
        calls function to update the current status and displays it to the console.
        '''
        if not self.pet:
            return
        status = self.pet.show_status()
        self.update_status(status)

    def show_image(self, image_path):  ### Goda 28.07.2024: Function to show images
        '''
        Display an image in a new window.
        '''
        window = tk.Toplevel(self.root)
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tk.Label(window, image=img)
        panel.image = img  # Keep a reference to avoid garbage collection
        panel.pack()
        window.mainloop()

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualPetApp(root)
    root.mainloop()
