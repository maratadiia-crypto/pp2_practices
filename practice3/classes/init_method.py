class Person:  # creates a class named person
  def __init__(self, name, age, city, country): # initializes the object's attributes
    self.name = name   #name
    self.age = age   #age
    self.city = city     #city
    self.country = country    #country

p1 = Person("Linus", 30, "Oslo", "Norway")  #creates a person 1 and initializes its atributes

print(p1.name)  #prints linus
print(p1.age)    #prints 30
print(p1.city)   #prints oslo
print(p1.country)   #prints norway