import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import time
import pygetwindow as gw

# Constants
gamma = 0.99  # Discount factor
epsilon = 1.0  # Exploration rate (no longer used)
max_episodes = 100000  # Define the number of training episodes
max_steps_per_episode = 10000
num_actions = 6  # Updated to include 'a', 'b', 'up', 'down', 'left', 'right'

# Create PyBoy instance and load the ROM
rom_path = 'C:\\pokemonRL\\retro-data\\roms\\gba\\PokemonRed.gb'
pyboy = PyBoy(rom_path)

# Wait for the emulator window to appear
while not gw.getWindowsWithTitle("PyBoy"):
    time.sleep(1)

# Constants for PyBoy button key codes
BUTTONS = {
    0: WindowEvent.PRESS_ARROW_UP,
    1: WindowEvent.PRESS_ARROW_DOWN,
    2: WindowEvent.PRESS_ARROW_LEFT,
    3: WindowEvent.PRESS_ARROW_RIGHT,
    4: WindowEvent.PRESS_BUTTON_A,
    5: WindowEvent.PRESS_BUTTON_B
}

# Action mapping function
def map_action_to_pyboy_input(action):
    # Send button press event
    pyboy.send_input(BUTTONS[action])
    time.sleep(0.1)  # Pause for 0.1 seconds after each action

    # Send button release event
    pyboy.send_input(BUTTONS[action] + 1)

# Define a simple convolutional neural network model
def create_model(input_shape, num_actions):
    model = Sequential([
        Conv2D(32, (8, 8), strides=(4, 4), activation='relu', input_shape=input_shape),
        Conv2D(64, (4, 4), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), strides=(1, 1), activation='relu'),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(num_actions)
    ])
    return model

# Preprocess game state
def preprocess_state(screen_image):
    state = np.array(screen_image.resize((160, 144)))  # Resize image
    state = state[:, :, :3]  # Keep only the first 3 channels (RGB), discard the 4th channel (usually alpha)
    state = state / 255.0  # Normalize
    return np.expand_dims(state, axis=0)

# Initialize model and target model
input_shape = (144, 160, 3)  # Screen resolution and RGB channels
model = create_model(input_shape, num_actions)
target_model = create_model(input_shape, num_actions)
target_model.set_weights(model.get_weights())  # Initialize target model weights

# Compile model
optimizer = Adam(learning_rate=0.00025, clipnorm=1.0)
model.compile(optimizer=optimizer, loss='mse')

render_every_n_steps = 50  # Render the screen every 50 steps

try:
    for episode in range(max_episodes):
        state = preprocess_state(pyboy.screen.image)  # Get initial state (screen image)
        episode_reward = 0

        for step in range(max_steps_per_episode):
            # Choose action randomly
            action = random.choice(range(num_actions))

            # Map the numeric action to the emulator's control
            map_action_to_pyboy_input(action)

            # Debug print action chosen
            print(f"Step {step}, Action chosen: {action}")

            # Render the screen and preprocess the next state
            if step % render_every_n_steps == 0:
                next_state = preprocess_state(pyboy.screen.image)
            else:
                # Skip rendering but still update state
                pyboy.tick()  # Update game state without rendering
                continue

            reward = 0  # Define your reward mechanism based on game state
            done = False  # Define when episode ends based on game state

            # Update Q-values using the Bellman equation
            if not done:
                target = reward + gamma * np.max(target_model.predict(next_state)[0])
            else:
                target = reward

            q_values_target = model.predict(state)
            q_values_target[0][action] = target
            model.fit(state, q_values_target, epochs=1, verbose=0)

            state = next_state
            episode_reward += reward

            if done:
                break

        # Print progress
        print(f"Episode: {episode + 1}/{max_episodes}, Reward: {episode_reward}")

        # Update target model weights every 10 episodes
        if episode % 10 == 0:
            target_model.set_weights(model.get_weights())

finally:
    pyboy.stop()  # Stop the PyBoy instance
    print("Emulator stopped")
