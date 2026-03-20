import os

os.makedirs("test_folder/inside_folder", exist_ok=True)
print("Folders created.")

print("Current directory:")
print(os.getcwd())

print("Contents:")
for item in os.listdir():
    print(item)