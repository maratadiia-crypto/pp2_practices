# define the parent class Person
class Person:
    # constructor of Person
    def __init__(self, name):
        self.name = name  

    # Method in parent class
    def greet(self):
        print("Hello, my name is", self.name)  # simple greeting

# define the child class Student that inherits from Person
class Student(Person):
    # constructor of Student
    def __init__(self, name, year):
        super().__init__(name)  # call the constructor of the parent class to set name
        self.year = year        # add a new attribute for the student's year

    # overriding the greet() method from the parent class
    def greet(self):
        # this greet() replaces the one in Person for Student objects
        print("Hello, my name is", self.name, "and I am in year", self.year)

# create an object of the parent class
p = Person("Alice")  
p.greet()            # Calls the greet() method of Person
# Output: Hello, my name is Alice

# create an object of the child class
s = Student("Bob", 3)  
s.greet()              # Calls the greet() method of Student (overridden)
# Output: Hello, my name is Bob and I am in year 3
