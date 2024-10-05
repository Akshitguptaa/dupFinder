import hashlib
import shutil
import os

def get_hash(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):  
            h.update(chunk)
    return h.hexdigest()  

def find_dups(dir_path):
    seen = {}
    dups = []

    for folder, _, files in os.walk(dir_path):
        for file in files:
            path = os.path.join(folder, file)
            file_hash = get_hash(path)

            if file_hash in seen:
                dups.append((seen[file_hash], path))
            else:
                seen[file_hash] = path

    return dups

def manage_dups(dups):
    if not dups:
        print("No duplicate file found!!!")
        return

    print("Duplicate files found:")
    for orig, dup in dups:
        print(f"Original-> {orig} \nDuplicate-> {dup}\n")

    action = input("Would you like to (d)elete or (m)ove the duplicates? (d/m): ")
    action=action.lower()
    if action == 'd':
        for _, dup in dups:
            os.remove(dup)  
            print(f"Deleted-> {dup}")
    elif action == 'm':
        target = input("Enter the target folder to move duplicates = ")
        if not os.path.exists(target):
            os.makedirs(target)  
        for _, dup in dups:
            shutil.move(dup, target)  
            print(f"Moved-> {dup} to {target}")

if __name__ == "__main__":
    dir_path = input("Enter the directory path to you want to scan = ")

    if os.path.exists(dir_path):
        dups = find_dups(dir_path)  
        manage_dups(dups) 
        print("Task completed!!!")
    else:
        print("ERROR!!, directory does not exist...")
