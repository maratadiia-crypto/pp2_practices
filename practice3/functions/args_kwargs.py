def my_function(title, *args, **kwargs):
  # title is a required argument
   # *args collects extra positional arguments into a tuple
    # **kwargs collects keyword arguments into a dictionary
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")

#it will output "User Info" as a title,
#   "Emil", "Tobias" as a "Positional arguments:" (args)
# age, 25, city ,"Oslo" as a "Keyword arguments:" (kwargs)