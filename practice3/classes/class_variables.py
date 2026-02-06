class Person:    
  species = "Human" # Class property (shared by all instances)

  def __init__(self, name):
    self.name = name # Instance property (unique to each object)

p1 = Person("Emil")
p2 = Person("Tobias")

print(p1.name)     # Emil
print(p2.name)     # Tobias
print(p1.species)  # Human
print(p2.species)  # Human