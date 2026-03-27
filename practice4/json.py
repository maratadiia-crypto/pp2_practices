
import json

# 1. Parsing JSON string using json.loads()
json_string = '{"name": "Adiya", "age": 17, "city": "Almaty"}'
python_data = json.loads(json_string)

print("JSON string converted to Python dictionary:")
print(python_data)
print("Name:", python_data["name"])
print("Age:", python_data["age"])
print("City:", python_data["city"])

print("-" * 40)

# 2. Converting Python object to JSON using json.dumps()
student = {
    "name": "Adiya",
    "age": 17,
    "university": "KBTU",
    "skills": ["Python", "Math", "Physics"]
}

student_json = json.dumps(student, indent=4)
print("Python dictionary converted to JSON string:")
print(student_json)

print("-" * 40)

# 3. Writing JSON to a file
with open("student.json", "w", encoding="utf-8") as file:
    json.dump(student, file, indent=4, ensure_ascii=False)

print("Data was written to student.json")

print("-" * 40)

# 4. Reading JSON from a file
with open("student.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print("Data loaded from student.json:")
print(loaded_data)

print("-" * 40)

# 5. Working with sample JSON data
sample_data = {
    "company": "OpenAI",
    "employees": [
        {"name": "Ali", "position": "Developer"},
        {"name": "Aruzhan", "position": "Designer"},
        {"name": "Dias", "position": "Manager"}
    ]
}

# Save sample data
with open("sample-data.json", "w", encoding="utf-8") as file:
    json.dump(sample_data, file, indent=4, ensure_ascii=False)

# Read sample data
with open("sample-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Company:", data["company"])
print("Employees:")
for employee in data["employees"]:
    print(employee["name"], "-", employee["position"])