
import math
import random

# 1. Convert degree to radian
degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", radian)

print("-" * 40)

# 2. Area of a trapezoid
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
trapezoid_area = ((base1 + base2) * height) / 2
print("Expected Output:", trapezoid_area)

print("-" * 40)

# 3. Area of regular polygon
n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))
polygon_area = (n * (side ** 2)) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", polygon_area)

print("-" * 40)

# 4. Area of parallelogram
base = float(input("Length of base: "))
height_p = float(input("Height of parallelogram: "))
parallelogram_area = base * height_p
print("Expected Output:", parallelogram_area)

print("-" * 40)

numbers = [1, 2, 3, 4, 5]
print("Random number from 1 to 100:", random.randint(1, 100))
print("Random choice from list:", random.choice(numbers))
random.shuffle(numbers)
print("Shuffled list:", numbers)