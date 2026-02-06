class Person:  #creating parent class
    def __init__(self, fname, lname): #class atributes
        self.firstname = fname
        self.lastname = lname

    def printname(self):   # method to print the full name
        print(self.firstname, self.lastname)

x = Person("John", "Doe") # create an object of class Person 
x.printname()  # John Doe

class Student(Person):  # define a class Student that inherits from Person
    pass  

# create an object of class Student
y = Student("Mike", "Olsen")
y.printname()  # Mike Olsen
