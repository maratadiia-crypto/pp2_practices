def myfunc(n):   #create function
  return lambda a : a * n   #returns value, using lambda functions

mytripler = myfunc(3)  #creates a function that multiplies by 3

print(mytripler(11))  #calls lamda func with a = 11