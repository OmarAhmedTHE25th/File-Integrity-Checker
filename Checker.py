import json
from pathlib import Path
import hashlib

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as FILE:
        for chunk in iter(lambda: FILE.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_dir_hashes(dir_path):
    hashes = {}
    for item in Path(dir_path).iterdir():
        if item.is_file():
            hashes[item.name] = hash_file(item)
    return hashes

def save_hashes(hashes, json_path):
    with open(json_path, "w") as f:
        json.dump(hashes, f, indent=4)

def load_hashes(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def check_integrity(dir_path, saved_hashes):
    fresh_hashes = get_dir_hashes(dir_path)
    
    unique_to_saved = saved_hashes.keys() - fresh_hashes.keys()
    unique_to_fresh = fresh_hashes.keys() - saved_hashes.keys()
    
    results = {
        "missing": list(unique_to_saved),
        "added": list(unique_to_fresh),
        "tampered": []
    }

    common_keys = fresh_hashes.keys() & saved_hashes.keys()
    for name in common_keys:
        if saved_hashes[name] != fresh_hashes[name]:
            results["tampered"].append(name)
            
    return results

def main():
    while True:
        path = input("Enter Path: ")
        dir_path = Path(path)
        if dir_path.exists() and dir_path.is_dir():
            break
        print("Invalid path. Please enter an existing directory path.")

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
        hashes = get_dir_hashes(dir_path)
        save_hashes(hashes, json_file)
        print("Baseline initialized.")
    else:
        saved_hashes = load_hashes(json_file)
        results = check_integrity(dir_path, saved_hashes)
        
        if results["missing"]:
            print(f"File {results['missing']} is missing")
        if results["added"]:
            print(f"File {results['added']} is added")
        for name in results["tampered"]:
            print(f"File {name} has been tampered with")
        
        if not any(results.values()):
            print("All files are intact.")

if __name__ == "__main__":
    main()


