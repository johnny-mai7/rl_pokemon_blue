import hashlib

def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        checksum = hashlib.sha256(content).hexdigest()
    return checksum

# Replace 'PokemonEmerald.gba' with the actual path to your ROM file
rom_path = 'C:\\pokemonRL\\retro-data\\roms\\gba\\PokemonEmerald.gba'
expected_checksum = 'a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af'  # Replace with the expected checksum

actual_checksum = calculate_checksum(rom_path)

if actual_checksum == expected_checksum:
    print("Checksums match. ROM file is valid.")
else:
    print(f"Checksums do not match. Expected: {expected_checksum}, Actual: {actual_checksum}")
