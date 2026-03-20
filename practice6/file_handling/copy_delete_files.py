import shutil
import os

shutil.copy("data.txt", "data_backup.txt")
print("File copied.")

if os.path.exists("data_backup.txt"):
    os.remove("data_backup.txt")
    print("Backup file deleted.")
else:
    print("File not found.")