numbers = [1, 2, 3, 4, 5, 6, 7, 8]   #creates a list of numbers
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))  # filter only odd numbers using a lambda function
print(odd_numbers)   #ptints onle odd nums
