class Person:   # creates a class named person
  def __init__(self, name, age):
    #initializes persons name and age
    self.name = name
    self.age = age

  def get_info(self):   # self returns information about the person
    return f"{self.name} is {self.age} years old"

p1 = Person("Tobias", 28)  # create a person 1
print(p1.get_info())       # call the method and print the result
