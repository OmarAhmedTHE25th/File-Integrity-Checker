import json
from pathlib import Path
import hashlib

def hash_file(file_path):
    with open(file_path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()

while True:
    path = input("Enter Path: ")
    dir_path = Path(path)
    if dir_path.exists() and dir_path.is_dir():
        break
    print("Invalid path. Please enter an existing directory path.")
hashes = {}
json_file = Path("hashes.json")
while True:
    choice = input("Do you want manual reinitialization? (y for yes, n for no: ")
    choice = choice.lower()
    if choice == 'y' or choice == 'n':
        break
    print("Invalid input. Please Try again.")
if choice == 'y':
    json_file.unlink(missing_ok=True)



if not json_file.exists():

    for item in dir_path.iterdir():
        hashes[item.name] = hash_file(item)

    with open("hashes.json","w") as json_file:
        json.dump(hashes,json_file,indent=4)
else:
    fresh_hashes = {}
    for item in dir_path.iterdir():
        fresh_hashes[item.name] = hash_file(item)

    with open('hashes.json', 'r') as file:
        saved_hashes = json.load(file)

        unique_to_saved_hash = saved_hashes.keys() - fresh_hashes.keys()
        unique_to_fresh_hash = fresh_hashes.keys() - saved_hashes.keys()
        if unique_to_saved_hash:
            print(f"File {str(unique_to_saved_hash)} is missing")
        if unique_to_fresh_hash:
            print(f"File {str(unique_to_fresh_hash)} is added")


        common_keys = fresh_hashes.keys() & saved_hashes.keys()
        for name in common_keys:
            if saved_hashes[name] != fresh_hashes[name]:
                print(f"File {name} has been tampered with")
















