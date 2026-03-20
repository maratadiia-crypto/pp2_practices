names = ["Aida", "Dana", "Murat"]
ages = [19, 20, 18]

for index, name in enumerate(names, start=1):
    print(index, name)

print()

for name, age in zip(names, ages):
    print(name, age)