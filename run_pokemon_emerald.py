import retro
import os

# Path to the custom integrations folder
custom_integrations_path = "C:/pokemonRL/retro-data/custom_integrations/"
retro.data.Integrations.add_custom_path(custom_integrations_path)

# Check if your game is listed
game_name = "PokemonEmerald-GBA"  # Adjust this based on Gym Retro's naming convention
print(game_name in retro.data.list_games(inttype=retro.data.Integrations.ALL))

# Create the environment
env = retro.make(game_name, inttype=retro.data.Integrations.ALL)

# Now you can use 'env' to interact with your integrated game
