from pyboy import PyBoy
import pygetwindow as gw
import time
import numpy as np
import random

# Path to your Pokémon Red ROM file
rom_path = 'C:\\pokemonRL\\retro-data\\roms\\gba\\PokemonGold.gbc'

# Create PyBoy instance and load the ROM
pyboy = PyBoy(rom_path)

# Wait for the emulator window to appear
while not gw.getWindowsWithTitle("PyBoy"):
    time.sleep(1)

try:
    num_episodes = 100000000000000000000000000  # Define the number of training episodes

    while True:  # Continuous loop for actions
        # Set emulation speed (no speed limit)
        pyboy.set_emulation_speed(0)

        # Randomly choose action to perform
        action = random.choice(['a', 'b', 'up', 'left', 'right', 'down'])
        print(f"Performing action: {action}")
        pyboy.button(action)
        
        # Advance the emulator by one frame
        pyboy.tick()

        # Delay to simulate processing time (adjust as needed)
        time.sleep(0.01)  # Example delay of 0.01 seconds

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    pyboy.stop()  # Stop the PyBoy emulator instance
    print("Emulator stopped")
