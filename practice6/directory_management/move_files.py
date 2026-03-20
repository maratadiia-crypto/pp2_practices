import os
import shutil

os.makedirs("moved_files", exist_ok=True)

if os.path.exists("data.txt"):
    shutil.move("data.txt", "moved_files/data.txt")
    print("File moved.")
else:
    print("data.txt not found.")