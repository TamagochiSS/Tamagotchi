import time

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.hunger = 50  # Hunger level, 0 means not hungry, 100 means very hungry
        self.happiness = 50  # Happiness level, 0 means sad, 100 means very happy

    def feed(self):
        if self.hunger > 0:
            self.hunger -= 10
            if self.hunger < 0:
                self.hunger = 0
            print(f"{self.name} has been fed.")
        else:
            print(f"{self.name} is not hungry.")
        self.show_status()

    def play(self):
        self.happiness += 10
        if self.happiness > 100:
            self.happiness = 100
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        print(f"You played with {self.name}.")
        self.show_status()

    def show_status(self):
        print(f"{self.name}'s status:")
        print(f"  Age: {self.age} days")
        print(f"  Hunger: {self.hunger}")
        print(f"  Happiness: {self.happiness}")

    def age_pet(self):
        self.age += 1
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
        self.happiness -= 5
        if self.happiness < 0:
            self.happiness = 0
        print(f"\nA day has passed. {self.name} is now {self.age} days old.")
        self.show_status()

def main():
    name = input("What is the name of your virtual pet? ")
    pet = VirtualPet(name)
    print(f"Welcome {pet.name}!")

    action_count = 0

    while True:
        print("\nMain Menu:")
        print("1. Feed Pet")
        print("2. Play with Pet")
        print("3. Check Status")
        print("4. Quit")

        choice = input("Choose an option: ")
        if choice == "1":
            pet.feed()
        elif choice == "2":
            pet.play()
        elif choice == "3":
            pet.show_status()
        elif choice == "4":
            print(f"Goodbye! {pet.name} will miss you!")
            break
        else:
            print("Invalid choice, please try again.")

        action_count += 1

        # After every 4 actions, increment the pet's age
        if action_count >= 4:
            pet.age_pet()
            action_count = 0

        # Simulate passage of time
        time.sleep(1)

if __name__ == "__main__":
    main()
