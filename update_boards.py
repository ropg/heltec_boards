import requests
import hashlib
import os

repo = "heltec_boards"

# Fetch release data to get the tag name
response = requests.get(f"https://api.github.com/repos/ropg/{repo}/releases/latest")
release_data = response.json()
tag_name = release_data['tag_name']

# Define the download URL using the tag name
download_url = f"https://github.com/ropg/{repo}/archive/refs/tags/{tag_name}.zip"

# Download the zip file
print(f"Downloading {download_url}...")
os.system(f"wget {download_url}")

download_path = f"{tag_name}.zip"

# Get the size of the file
file_size = os.path.getsize(download_path)
print(f"file size: {file_size} bytes");

# Compute the SHA-256 hash of the file
sha256_hash = hashlib.sha256()
with open(download_path, 'rb') as f:
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
print(f"hash: {sha256_hash.hexdigest()}")

# Assuming boards.json needs to be updated with the file size and hash
with open('boards.json.editme', 'r') as file:
    content = file.read()

# Replace placeholders or update the content as needed
content = content\
    .replace('{repo}', repo)\
    .replace('{filesize}', str(file_size))\
    .replace('{hash}', sha256_hash.hexdigest())\
    .replace('{tag}', tag_name)

with open('boards.json', 'w') as file:
    file.write(content)

os.system(f"rm {download_path}");

print("boards.json has been updated.")
