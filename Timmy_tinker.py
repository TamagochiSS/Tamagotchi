import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import json # Lib for the JSON file format
import os # Library to help with the save utilily
import random 

SAVE_FILE = "pets_data.json"

class VirtualPet:
    def __init__(self, name, age=0, hunger=50, happiness=50, health=100, tiredness=50):
        self.name = name
        self.age = age  # In pet days
        self.hunger = hunger
        self.happiness = happiness
        self.health =  health 
        self.tiredness = tiredness 

    def feed(self):
        self.hunger = min(100, self.hunger + 5)
        if self.hunger > 0:
            self.hunger -= 10
            if self.hunger < 0:
                self.hunger = 0
            return f"{self.name} has been fed."
        else:
            return f"{self.name} is not hungry."

    def play(self, game_type):
        if game_type == "catch":
            self.happiness = min(100, self.happiness + 20)
            self.hunger = min(100, self.hunger + 10)
            self.tiredness = min(100, self.tiredness + 15)
        elif game_type == "puzzle":
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
        elif game_type == "dance":
            self.happiness = min(100, self.happiness + 10)
            self.health = min(100, self.health + 5)
            self.hunger = min(100, self.hunger + 5)
            self.tiredness = min(100, self.tiredness + 10)
        
        # Call the random_event function after playing
        event_played = self.random_event()
        
        return f"You played {game_type} with {self.name}. {event_played}"

    def vet(self):
        self.health = min(100, self.health + 20)
        self.happiness = max(0, self.happiness - 10)
        return f"{self.name} visited the vet."

    def sleep(self):
        self.tiredness = max(0, self.tiredness - 20)
        self.health = min(100, self.health + 10)
        self.happiness = max(0, self.happiness - 10)
        return f"{self.name} had a good sleep."

    def random_event(self):
        events = ["found a toy", "got hurt", "nothing happened"]
        event = random.choice(events)
        if event == "found a toy":
            self.happiness = min(100, self.happiness + 10)
            return f"{self.name} found a toy and is happier!"
        elif event == "got hurt":
            self.health = max(0, self.health - 10)
            return f"{self.name} got hurt while playing and lost some health."
        elif event == "nothing happened":
            return f"Nothing special happened to {self.name}."
        
    def show_status(self):
        return (f"{self.name}'s status:\n"
                f"  Age: {self.age} days\n"
                f"  Hunger: {self.hunger}\n"
                f"  Happiness: {self.happiness}\n"
                f"  Health: {self.health}\n"
                f"  Tiredness: {self.tiredness}") 

    # def feed(self):
    #     if self.hunger > 0:
    #         self.hunger -= 10
    #         if self.hunger < 0:
    #             self.hunger = 0
    #         return f"{self.name} has been fed."
    #     else:
    #         return f"{self.name} is not hungry."

    # def play(self):
    #     self.happiness += 10
    #     if self.happiness > 100:
    #         self.happiness = 100
    #     self.hunger += 5
    #     if self.hunger > 100:
    #         self.hunger = 100
    #     return f"You played with {self.name}."


    # def show_status(self):
    #     return (f"{self.name}'s status:\n"
    #             f"  Age: {self.age} pet days\n"
    #             f"  Hunger: {self.hunger}\n"
    #             f"  Happiness: {self.happiness}")

    def to_dict(self, real_time_elapsed, pet_time_elapsed):
        return {
            'name': self.name,
            'age': self.age,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'tiredness': self.tiredness,
            'health': self.health,
            'real_time_elapsed': real_time_elapsed,
            'pet_time_elapsed': pet_time_elapsed
        }

    @staticmethod
    def from_dict(data):
        return VirtualPet(data['name'], data['age'], data['hunger'], data['happiness'], data['tiredness'], data['health'])


class VirtualPetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")

        self.pet = None
        self.start_time = None  # Real start time
        self.real_seconds_elapsed = 0
        self.pet_seconds_elapsed = 0  # Pet time in seconds

        self.create_widgets()

        # Check for saved pet data
        self.load_pet_prompt()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Enter pet's name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack()

        self.load_button = tk.Button(self.root, text="Load", command=self.load_pet_prompt, state=tk.NORMAL)
        self.load_button.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_pet, state=tk.DISABLED)
        self.save_button.pack()

        self.feed_button = tk.Button(self.root, text="Feed", command=self.feed, state=tk.DISABLED)
        self.feed_button.pack()

        self.play_button = tk.Button(self.root, text="Play", command=lambda: [self.play_catch_button.pack(), self.play_puzzle_button.pack(), self.play_dance_button.pack()], state=tk.DISABLED)
        self.play_button.pack()

        self.play_catch_button = tk.Button(self.root, text="Play Catch", command=lambda: self.play("catch"), state=tk.DISABLED)
        # self.play_catch_button.pack()

        # self.play_puzzle_button = tk.Button(self.root, text="Play Puzzle", command=lambda: [self.play("puzzle"), self.sleep_button.pack_forget()], state=tk.DISABLED)
        # self.play_puzzle_button.pack()

        self.play_puzzle_button = tk.Button(self.root, text="Play Puzzle", command=lambda: self.play("puzzle"), state=tk.DISABLED)
        # self.play_puzzle_button.pack()

        self.play_dance_button = tk.Button(self.root, text="Play Dance", command=lambda: self.play("dance"), state=tk.DISABLED)
        # self.play_dance_button.pack()

        self.sleep_button = tk.Button(self.root, text="Sleep", command=self.sleep, state=tk.DISABLED)
        self.sleep_button.pack()

        self.vet_button = tk.Button(self.root, text="Visit Vet", command=self.vet, state=tk.DISABLED)
        self.vet_button.pack()

        self.status_button = tk.Button(self.root, text="Check Status", command=self.show_status, state=tk.DISABLED)
        self.status_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, state=tk.DISABLED)
        self.quit_button.pack()

        self.status_text = tk.Text(self.root, height=15, width=80)
        self.status_text.pack()

        self.real_time_label = tk.Label(self.root, text="Real Time: 0s")
        self.real_time_label.pack()

        self.pet_time_label = tk.Label(self.root, text="Pet Time: 0 pet days")
        self.pet_time_label.pack()

        # self.play_catch_button.pack_forget() 

    def start(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name for your pet.")
            return

        self.pet = VirtualPet(name)
        self.start_time = time.time()  # Set the start time
        self.real_seconds_elapsed = 0  # Initialize real time elapsed
        self.pet_seconds_elapsed = 0  # Initialize pet time elapsed
        self.update_status(f"Welcome {self.pet.name}!")

        self.save_button.config(state=tk.NORMAL)
        self.feed_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.play_catch_button.config(state=tk.NORMAL)
        self.play_puzzle_button.config(state=tk.NORMAL)
        self.play_dance_button.config(state=tk.NORMAL)
        self.sleep_button.config(state=tk.NORMAL)
        self.vet_button.config(state=tk.NORMAL)
        self.status_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.load_button.config(state=tk.DISABLED)
        self.name_entry.config(state=tk.DISABLED)

        self.update_times()
        self.update_pet_time()

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
                    messagebox.showerror("Error", "Pet not found.")
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

                    self.update_status(f"Welcome back {self.pet.name}!") # Welcome message

                    self.save_button.config(state=tk.NORMAL)
                    self.feed_button.config(state=tk.NORMAL)
                    self.play_button.config(state=tk.NORMAL)
                    self.play_catch_button.config(state=tk.NORMAL)
                    self.play_puzzle_button.config(state=tk.NORMAL)
                    self.play_dance_button.config(state=tk.NORMAL)
                    self.sleep_button.config(state=tk.NORMAL)
                    self.vet_button.config(state=tk.NORMAL)
                    self.status_button.config(state=tk.NORMAL)
                    self.quit_button.config(state=tk.NORMAL)
                    self.start_button.config(state=tk.DISABLED)
                    self.load_button.config(state=tk.DISABLED)
                    self.name_entry.config(state=tk.DISABLED)

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
            self.real_time_label.config(text=f"Real Time: {self.format_real_time(self.real_seconds_elapsed)}")

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

            self.pet_time_label.config(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

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
        if not self.pet:
            return
        result = self.pet.feed()
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def play(self, game_type):
        if not self.pet:
            return
        result = self.pet.play(game_type)
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def sleep(self):
        if not self.pet:
            return
        result = self.pet.sleep()
        self.update_status(result)
        self.advance_pet_time(2 * 3600)  # Advance pet time by 2 pet hours (converted to seconds)

    def vet(self):
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
        self.pet_time_label.config(text=f"Pet Time: {self.format_pet_time(self.pet_seconds_elapsed)}")

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
