import tkinter as tk
from tkinter import messagebox
import time

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.age = 0  # In pet days
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
        if (self.hunger > 100):
            self.hunger = 100
        return f"You played with {self.name}."

    def show_status(self):
        return (f"{self.name}'s status:\n"
                f"  Age: {self.age} pet days\n"
                f"  Hunger: {self.hunger}\n"
                f"  Happiness: {self.happiness}")

class VirtualPetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")

        self.pet = None
        self.start_time = None  # Real start time
        self.real_seconds_elapsed = 0
        self.pet_seconds_elapsed = 0  # Pet time in seconds

        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Enter pet's name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack()

        self.feed_button = tk.Button(self.root, text="Feed", command=self.feed, state=tk.DISABLED)
        self.feed_button.pack()

        self.play_button = tk.Button(self.root, text="Play", command=self.play, state=tk.DISABLED)
        self.play_button.pack()

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

        self.feed_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.status_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        self.update_times()
        self.update_pet_time()

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

        # Schedule the update_pet_time method to run again after 1000ms (1s)
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

    def play(self):
        if not self.pet:
            return
        result = self.pet.play()
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
