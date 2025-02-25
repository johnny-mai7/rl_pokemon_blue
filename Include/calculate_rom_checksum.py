import hashlib

def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        checksum = hashlib.sha256(content).hexdigest()
    return checksum

# Replace 'PokemonEmerald.gba' with the actual path to your ROM file
rom_path = 'C:\\pokemonRL\\retro-data\\roms\\gba\\PokemonEmerald.gba'

actual_checksum = calculate_checksum(rom_path)
print(f"Checksum: {actual_checksum}")
