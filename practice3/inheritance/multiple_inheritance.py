
class Person:  # first parent class
    def __init__(self, name):
        self.name = name  
    def greet(self):   # method of Person
        print("Hello, my name is", self.name)

class School:  # second parent class
    def __init__(self, school_name):
        self.school_name = school_name  # Store school name

    def school_info(self):      # method of School
        print("I study at", self.school_name)

class Student(Person, School):  # child class with multiple inheritance
    def __init__(self, name, school_name, year):
       # call constructors of both parent classes
        Person.__init__(self, name)       # initialize name from Person
        School.__init__(self, school_name) # initialize school_name from School
        self.year = year                  # add new attribute for year

    
    def student_info(self):  # additional method of Student
        print("I am in year", self.year)


s = Student("Alice", "Greenwood High", 3)  # create a Student object

# call methods inherited from both parents
s.greet()         
# Output: Hello, my name is Alice

s.school_info()   
# Output: I study at Greenwood High

s.student_info()  
# Output: I am in year 3
