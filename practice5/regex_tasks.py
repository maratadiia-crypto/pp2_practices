import re   # import module for working with regular expressions

# 1. Match a string that has 'a' followed by zero or more 'b'
# regex pattern: ab*
text1 = "abbb"        # example string
pattern1 = r"ab*"     # 'a' followed by zero or more 'b'

# re.fullmatch checks if the whole string matches the pattern
if re.fullmatch(pattern1, text1):
    print("1. Match found")
else:
    print("1. No match")


# 2. Match 'a' followed by two to three 'b'
# regex pattern: ab{2,3}
text2 = "abbb"        # example string
pattern2 = r"ab{2,3}" # 'a' followed by 2 or 3 'b'

if re.fullmatch(pattern2, text2):
    print("2. Match found")
else:
    print("2. No match")


# 3. Find sequences of lowercase letters joined with underscore
# example: hello_world
# regex: [a-z]+_[a-z]+

text3 = "hello_world test_case example_text"

# pattern finds lowercase words connected with underscore
pattern3 = r"[a-z]+_[a-z]+"

# re.findall returns all matches in the string
print("3.", re.findall(pattern3, text3))


# 4. Find sequences of one uppercase letter followed by lowercase letters
# example: Hello World
# regex: [A-Z][a-z]+
text4 = "Hello World Python Programming"

# pattern finds words that start with capital letter
pattern4 = r"[A-Z][a-z]+"

print("4.", re.findall(pattern4, text4))


# 5. Match 'a' followed by anything, ending in 'b'
# regex: a.*b
text5 = "axxxb"

# .* means any characters any number of times
pattern5 = r"a.*b"

if re.fullmatch(pattern5, text5):
    print("5. Match found")
else:
    print("5. No match")


# 6. Replace spaces, commas or dots with colon
# regex: [ ,.]
text6 = "Hello, world. Python is fun"

# re.sub replaces all characters that match the pattern
# here we replace space, comma and dot with colon
result6 = re.sub(r"[ ,.]", ":", text6)

print("6.", result6)


# 7. Convert snake_case string to camelCase
# example: my_variable_name -> myVariableName
def snake_to_camel(text):
    # pattern finds underscore followed by a letter
    # the lambda function makes the letter uppercase
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

text7 = "my_variable_name"
print("7.", snake_to_camel(text7))


# 8. Split a string at uppercase letters
# example: HelloWorldPython -> ['Hello', 'World', 'Python']
text8 = "HelloWorldPython"

# (?=[A-Z]) means split before capital letters
result8 = re.split(r"(?=[A-Z])", text8)

print("8.", result8)


# 9. Insert spaces between words starting with capital letters
# example: HelloWorld -> Hello World
text9 = "HelloWorldPython"

# (?<!^) ensures we do not insert space at the beginning
# ([A-Z]) finds capital letters
result9 = re.sub(r"(?<!^)([A-Z])", r" \1", text9)

print("9.", result9)


# 10. Convert camelCase to snake_case
# example: myVariableName -> my_variable_name

def camel_to_snake(text):
    # find capital letters and insert underscore before them
    # then convert everything to lowercase
    return re.sub(r"([A-Z])", r"_\1", text).lower()

text10 = "myVariableName"
print("10.", camel_to_snake(text10))