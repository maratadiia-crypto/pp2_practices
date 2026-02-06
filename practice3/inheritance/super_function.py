# define the Person class
class Person:
    def __init__(self, fname, lname):  #stores atributes of person
        self.firstname = fname  
        self.lastname = lname   

# creates the Student class that inherits from Person
class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)  # call the constructor of the parent class
        self.graduationyear = year      # add a new attribute for graduation year

    # method to welcome the student
    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

# create a Student object
s1 = Student("Mike", "Olsen", 2026)
s1.welcome()  # output: Welcome Mike Olsen to the class of 2026
