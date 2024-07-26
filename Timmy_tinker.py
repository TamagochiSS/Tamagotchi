import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import time
import json  # Lib for the JSON file format
import os  # Library to help with the save utilily
import random 
import customtkinter
import customtkinter as ctk

SAVE_FILE = "pets_data.json"

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

class VirtualPet:
    '''
    VirtualPet class, holding all functions to change the pets properties/statistics
    '''
    def __init__(self, name, age=0, hunger=50, happiness=50, health=100, tiredness=50, intellect=0):
        ''' Constructor to initialize a VirtualPet instance, used with default parameters as all pets are supposed 
        to start with the same preconditions.
        '''
        self.name = name
        self.age = age  # In pet days
        self.hunger = hunger
        self.happiness = happiness
        self.health =  health 
        self.tiredness = tiredness 
        self.intellect =  intellect 

    def feed(self):
        '''
        feed VirtualPet and change hunger score
        '''
        self.hunger = min(100, self.hunger + 5)
        if self.hunger > 0:
            self.hunger -= 10
            if self.hunger < 0:
                self.hunger = 0
            return f"{self.name} has been fed."
        else:
            return f"{self.name} is not hungry."

    def play(self, game_type):
        '''
        play with VirtualPet. pet statistics change depending on game_type
        
        Parameters
        ----------
        game_type: str
            defines which game the pet is playing 
        '''
        if game_type == "hide and seek":
            self.happiness = min(100, self.happiness + 20)
            self.hunger = min(100, self.hunger + 10)
            self.tiredness = min(100, self.tiredness + 15)
        elif game_type == "memory":
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
            self.intellect = min(100, self.intellect + 5)
        elif game_type == "beachball":
            self.happiness = min(100, self.happiness + 10)
            self.health = min(100, self.health + 5)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
        
        # Call the random_event function after playing to print random event to console
        event_played = self.random_event()
        
        return f"You played {game_type} with {self.name}. {event_played}"


    def TV(self, show_type):
        if show_type == "cartoon":
            self.happiness = min(100, self.happiness + 20)
            self.hunger = min(100, self.hunger + 10)
            self.tiredness = min(100, self.tiredness + 15)
            self.intellect = max(0, self.intellect - 10)
        elif show_type == "documentary":
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
            self.intellect = min(100, self.intellect + 5)

        # Create random show
       
       # Call random_show function for watching TV
       # show_watched = self.random_show()
        
       # return f"You watched {show_type} with {self.name}. {show_watched}"


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
        self.tiredness = max(0, self.tiredness - 20)
        self.health = min(100, self.health + 10)
        self.happiness = max(0, self.happiness - 10)
        return f"{self.name} had a good sleep."

    def random_event(self):
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
            self.health = max(0, self.health - 10)
            self.intellect = max(0, self.intellect - 10)
            return f"{self.name} lost balance and stumbled. You should get a plaster and some sweets."
        elif event == "nothing happened":
            return f"{self.name} is very calm today."
        
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
        pet = VirtualPet(data['name'], data['age'], data['hunger'], data['happiness'], data['tiredness'], data['health'], data['intellect'])
        pet.selected_animal = data.get('selected_animal', 'cat')  # Judit – 25.07.2024: Default to 'cat' if not found
        return pet

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
        self.load_pet_prompt() # Check for saved pet data
    
    def load_images(self):  # Judit – 25.07.2024: Load and scale images once
        '''
    	
        '''
        self.animal_options = ["cat", "chicken", "shrimp", "sheep"]
        self.animal_images = {}
        for animal in self.animal_options:
            image_path = os.path.join('pet_pictures', f'picture_{animal}.png')  # Adjusted path to the images folder
            if not os.path.exists(image_path):
                continue
            image = Image.open(image_path)
            resized_image = image.resize((100, 100), Image.LANCZOS)  # Resize the image to a smaller format
            self.animal_images[animal] = ImageTk.PhotoImage(resized_image)
        
        # Load button images
        self.play_image = ImageTk.PhotoImage(Image.open('buttons/play_button.png').resize((50, 50), Image.LANCZOS))  # Judit – 25.07.2024
        self.feed_image = ImageTk.PhotoImage(Image.open('buttons/feed_button.png').resize((50, 50), Image.LANCZOS))  # Judit – 25.07.2024
        self.TV_image = ImageTk.PhotoImage(Image.open('buttons/tv_button.png').resize((50, 50), Image.LANCZOS))  # Judit – 25.07.2024
        self.sleep_image = ImageTk.PhotoImage(Image.open('buttons/sleep_button.png').resize((50, 50), Image.LANCZOS))  # Judit – 25.07.2024
        self.vet_image = ImageTk.PhotoImage(Image.open('buttons/vet_button.png').resize((50, 50), Image.LANCZOS))  # Judit – 25.07.2024

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
        '''
        
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(pady=10)

        self.middle_frame = ctk.CTkFrame(self.root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = ctk.CTkFrame(self.root)
        self.bottom_frame.pack(pady=10)

        self.time_frame = ctk.CTkFrame(self.root)
        self.time_frame.pack(pady=10)
        
        # Top Frame Widgets
        self.name_label = customtkinter.CTkLabel(self.top_frame, text="Enter pet's name:")
        self.name_label.pack(side="left", padx=5)

        self.name_entry = customtkinter.CTkEntry(self.top_frame)
        self.name_entry.pack(side="left", padx=5)
        # Middle Frame Widgets
        self.start_button = customtkinter.CTkButton(self.middle_frame, text="Start", command=self.start)
        self.start_button.pack(side="left", padx=5)

        self.load_button = customtkinter.CTkButton(self.middle_frame, text="Load", command=self.load_pet_prompt)
        self.load_button.pack(side="left", padx=5)

        self.save_button = customtkinter.CTkButton(self.middle_frame, text="Save", command=self.save_pet, state="disabled")
        self.save_button.pack(side="left", padx=5)

        self.feed_button = customtkinter.CTkButton(self.middle_frame, text="Feed", image=self.feed_image, compound="top", command=self.feed, state="disabled")  # Judit – 25.07.2024
        self.feed_button.pack(side="left", padx=5)

        self.play_button = customtkinter.CTkButton(self.middle_frame, text="Play", image=self.play_image, compound="top", command=self.show_play_buttons, state="disabled")  # Judit – 25.07.2024
        self.play_button.pack(side="left", padx=5)

        self.play_hideandseek_button = customtkinter.CTkButton(self.root, text="Play hide and seek", command=lambda: self.play("hide and seek"))
         # self.play_puzzle_button = tk.Button(self.root, text="Play Puzzle", command=lambda: [self.play("puzzle"), self.sleep_button.pack_forget()], state=tk.DISABLED)
        self.play_memory_button = customtkinter.CTkButton(self.root, text="Play memory", command=lambda: self.play("memory"))
        self.play_beachball_button = customtkinter.CTkButton(self.root, text="Play beachball", command=lambda: self.play("beachball"))

        self.TV_button = customtkinter.CTkButton(self.middle_frame, text="Watch TV", image=self.TV_image, compound="top", command=self.TV, state="disabled")  # Judit – 25.07.2024
        self.TV_button.pack(side="left", padx=5)

        self.sleep_button = customtkinter.CTkButton(self.middle_frame, text="Sleep", image=self.sleep_image, compound="top", command=self.sleep, state="disabled")  # Judit – 25.07.2024
        self.sleep_button.pack(side="left", padx=5)

        self.vet_button = customtkinter.CTkButton(self.middle_frame, text="Visit Vet", image=self.vet_image, compound="top", command=self.vet, state="disabled")  # Judit – 25.07.2024
        self.vet_button.pack(side="left", padx=5)

        self.status_button = customtkinter.CTkButton(self.middle_frame, text="Check Status", command=self.show_status, state="disabled")
        self.status_button.pack(side="left", padx=5)

        self.quit_button = customtkinter.CTkButton(self.middle_frame, text="Quit", command=self.root.quit, state="disabled")
        self.quit_button.pack(side="left", padx=5)
        # Bottom Frame Widgets
        self.status_text = customtkinter.CTkTextbox(self.bottom_frame, height=140, width=550)
        self.status_text.pack(side="left", padx=5)

   # Time Frame Widgets
        self.real_time_label = customtkinter.CTkLabel(self.time_frame, text="Real Time: 0s", text_color="darkgreen")
        self.real_time_label.pack(side="left", padx=10)

        self.pet_time_label = customtkinter.CTkLabel(self.time_frame, text="Pet Time: 0 pet days", text_color="darkgreen")
        self.pet_time_label.pack(side="left", padx=10)
        
        self.pet_image_label = tk.Label(self.root)
        self.pet_image_label.pack()  # To display the selected pet's image after naming
        
         # self.play_hideandseek_button.pack_forget() 

    def show_play_buttons(self):
        '''
        function to display play buttons to choose from different play activities.
        '''
        self.play_hideandseek_button.pack(pady=5)
        self.play_memory_button.pack(pady=5)
        self.play_beachball_button.pack(pady=5)
        
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
        self.pet_image_label.config(image=self.animal_images[self.selected_animal])  # Display selected pet's image
        self.save_button.configure(state=tk.NORMAL)
        self.feed_button.configure(state=tk.NORMAL)
        self.play_button.configure(state=tk.NORMAL)
        self.TV_button.configure(state=tk.NORMAL)
        self.play_hideandseek_button.configure(state=tk.NORMAL)
        self.play_memory_button.configure(state=tk.NORMAL)
        self.play_beachball_button.configure(state=tk.NORMAL)
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
        self.animal_label = tk.Label(self.root, text="Wähle ein Tier:")
        self.animal_label.pack()

        self.animal_buttons = {}
        button_frame = tk.Frame(self.root)  # Create a frame to hold the buttons
        button_frame.pack()

        for animal in self.animal_options:
            self.animal_buttons[animal] = tk.Button(button_frame, image=self.animal_images[animal], command=lambda a=animal: self.select_animal(a))
            self.animal_buttons[animal].pack(side=tk.LEFT, padx=10, pady=10)  # Add padding for spacing

    def select_animal(self, animal):
        self.selected_animal = animal

        for button in self.animal_buttons.values():
            button.pack_forget()
        self.animal_label.pack_forget()

        self.create_name_widgets()

    def create_name_widgets(self):
        self.name_label.pack()
        self.name_entry.pack()
        self.start_button.pack()

    def load_pet_prompt(self): #Definition used for loading prompt when game starts
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file: # Read mode
                pets_data = json.load(file)
            pet_names = list(pets_data.keys())
            if pet_names:
                pet_name = simpledialog.askstring("Load Pet", "Enter the name of the pet to load:", initialvalue=pet_names[0])
                if pet_name and pet_name in pet_names:
                    self.load_pet(pet_name)
                else:
                    self.pet_not_found()  # Judit – 25.07.2024: Trigger the pet not found process
            else:
                messagebox.showinfo("Info", "No saved pets available.")

    def load_pet(self, pet_name): #Logic for loading old pet.
        try:
            with open(SAVE_FILE, "r") as file: #reads saved file
                pets_data = json.load(file)
                if pet_name in pets_data:
                    pet_data = pets_data[pet_name]
                    self.pet = VirtualPet.from_dict(pet_data)
                    self.real_seconds_elapsed = pet_data['real_time_elapsed']
                    self.pet_seconds_elapsed = pet_data['pet_time_elapsed']
                    self.start_time = time.time() - self.real_seconds_elapsed
                    self.selected_animal = pet_data.get('selected_animal', 'cat')  # Judit – 25.07.2024: Default to 'cat' if not found
                    self.update_status(f"Welcome back {self.pet.name}!") # Welcome message
                    self.pet_image_label.config(image=self.animal_images[self.selected_animal])  # Display the selected pet's image
                    self.save_button.configure(state=tk.NORMAL)
                    self.feed_button.configure(state=tk.NORMAL)
                    self.play_button.configure(state=tk.NORMAL)
                    self.TV_button.configure(state=tk.NORMAL)
                    self.play_hideandseek_button.configure(state=tk.NORMAL)
                    self.play_memory_button.configure(state=tk.NORMAL)
                    self.play_beachball_button.configure(state=tk.NORMAL)
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

    def save_pet(self): #Definition used to save current playing pet
        if not self.pet:
            return
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as file:
                    pets_data = json.load(file)
            else:
                pets_data = {}

            pets_data[self.pet.name] = self.pet.to_dict(self.real_seconds_elapsed, self.pet_seconds_elapsed)

            with open(SAVE_FILE, "w") as file: # Sets Write mode
                json.dump(pets_data, file, indent=4)

            self.update_status(f"{self.pet.name}'s data has been saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save pet: {e}")

    def update_times(self):
        if self.pet:
            # Real time elapsed since start
            current_time = time.time()
            real_time_elapsed = current_time - self.start_time
            self.real_seconds_elapsed = int(real_time_elapsed)
            self.real_time_label.configure(text=f"Real Time: {self.format_real_time(self.real_seconds_elapsed)}")

        # Schedule the update_times method to run again after 1000ms (1s)
        self.root.after(1000, self.update_times)

    def update_pet_time(self):
        if self.pet:
            # Update pet time independently
            self.pet_seconds_elapsed += 3600/24  # Increment pet time by 1 pet hour (3600 pet seconds)
            pet_days_elapsed = self.pet_seconds_elapsed / (24 * 60 * 60)
            old_age = self.pet.age
            self.pet.age = int(pet_days_elapsed)  # Update pet age in pet days
            if self.pet.age > old_age:
                self.update_status(f"A new pet day has passed. {self.pet.name} is now {self.pet.age} pet days old.")

            self.pet_time_label.configure(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

        # Schedule the update_pet_time method to run again after 1s
        self.root.after(1000, self.update_pet_time)

    def format_real_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def format_pet_time(self, pet_seconds):
        pet_hours, pet_seconds = divmod(pet_seconds, 3600)
        pet_days, pet_hours = divmod(pet_hours, 24)
        pet_minutes, pet_seconds = divmod(pet_seconds, 60)
        return f"{int(pet_days)} pet days {int(pet_hours)}h {int(pet_minutes)}m {int(pet_seconds)}s"

    def feed(self):
        '''
        action caused by clicking feed-button. Calls feed function of pet.
        '''
        if not self.pet:
            return
        result = self.pet.feed()
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def play(self, game_type):
        '''
        Action caused by clicking play-button. Calls play function of pet.
        '''
        if not self.pet:
            return
        result = self.pet.play(game_type)
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def TV(self, show_type): 
        '''
        Action causes by clicking TV-button. Calls ?
        '''
        if not self.pet:
            return
        result = self.pet.play(show_type)
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)


    def sleep(self):
        '''
        Action caused by clicking sleep button. Calls sleep function of VirtualPet.
        '''
        if not self.pet:
            return
        result = self.pet.sleep()
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def vet(self):
        '''
        Action caused by vet button. Calls vet function of VirtualPet.
        '''
        if not self.pet:
            return
        result = self.pet.vet()
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def advance_pet_time(self, seconds):
        
        self.pet_seconds_elapsed += seconds  # Advance pet time by given seconds
        pet_days_elapsed = self.pet_seconds_elapsed / (24 * 60 * 60)
        old_age = self.pet.age  
        self.pet.age = int(pet_days_elapsed)  # Update pet age in pet days
        if self.pet.age > old_age:
            self.update_status(f"A new pet day has passed. {self.pet.name} is now {self.pet.age} pet days old.")
        self.pet_time_label.configure(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

    def show_status(self):
        if not self.pet:
            return
        status = self.pet.show_status()
        self.update_status(status)

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)

if __name__ == "__main__":

    root = tk.Tk()
    app = VirtualPetApp(root)
    root.mainloop()
