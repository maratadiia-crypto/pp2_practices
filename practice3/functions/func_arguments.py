def my_function(country = "Norway"):   #creating a function with default argument country = norway
  print("I am from", country)

my_function("Sweden")    #calls a func with argument as "sweden"
my_function("India")   #calls a func with argument as "sweden"
my_function()      #calls a func without argument (will use norway, as default argument)
my_function("Brazil")     #calls a func with argument as "sweden"