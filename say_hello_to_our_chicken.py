import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas, PhotoImage

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


class VirtualPetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")

        self.pet = None
        self.action_count = 0

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

        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.pack()

    def start(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name for your pet.")
            return

        self.pet = VirtualPet(name)
        self.update_status(f"Welcome {self.pet.name}!")

        # Create the Canvas widget and store it as an attribute – Judit: 09.07.
        self.canvas = Canvas(self.root, width=500, height=400, background='gray75')
        self.canvas.pack()

        # Load the image and store it as an attribute – Judit: 09.07.
        self.myimg = PhotoImage(file='DALL_E_chicken.png')
        self.canvas.create_image(10, 10, image=self.myimg, anchor='nw')

        self.feed_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.status_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

    def feed(self):
        if not self.pet:
            return
        result = self.pet.feed()
        self.update_status(result)
        self.increment_action_count()

    def play(self):
        if not self.pet:
            return
        result = self.pet.play()
        self.update_status(result)
        self.increment_action_count()

    def show_status(self):
        if not self.pet:
            return
        status = self.pet.show_status()
        self.update_status(status)

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)

    def increment_action_count(self):
        self.action_count += 1
        if self.action_count >= 4:
            result = self.pet.age_pet()
            self.update_status(result)
            self.action_count = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualPetApp(root)
    root.mainloop()
