words = ["apple", "pie", "banana", "cherry"]  #creates a list of fruits (strings)
sorted_words = sorted(words, key=lambda x: len(x))  #sorts them by word length using lamda function
print(sorted_words)