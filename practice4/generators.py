
# 1. squares of numbers up to some number N.
def square_numbers(n):
    for i in range(n + 1):
        yield i * i

# 2.even numbers between 0 and n in comma separated form.
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

# 3.numbers divisible by 3 and 4 between 0 and n.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4 yield squares of numbers from a to b.
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

# 5.all numbers from n to 0.
def countdown(n):
    for i in range(n, -1, -1):
        yield i

if __name__ == "__main__":
    #1
    n1 = int(input("Enter N for square generator: "))
    print("Squares up to N:")
    for value in square_numbers(n1):
        print(value, end=" ")
    print()

    #2
    n2 = int(input("Enter n for even numbers: "))
    print("Even numbers:", ",".join(str(x) for x in even_numbers(n2)))

    #3
    n3 = int(input("Enter n for numbers divisible by 3 and 4: "))
    print("Divisible by 3 and 4:", ",".join(str(x) for x in divisible_by_3_and_4(n3)))

    #4
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    print("Squares from a to b:")
    for value in squares(a, b):
        print(value)

    #5
    n5 = int(input("Enter n for countdown: "))
    print("Countdown:", ",".join(str(x) for x in countdown(n5)))