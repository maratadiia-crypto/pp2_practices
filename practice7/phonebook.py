import csv
import os
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Table created successfully")

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (row["username"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Data imported from CSV successfully.")

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (username, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")

def update_contact():
    username = input("Enter username to update: ")

    print("1 - Update username")
    print("2 - Update phone")

    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        new_username = input("Enter new username: ")

        cur.execute(
            "UPDATE phonebook SET username=%s WHERE username=%s",
            (new_username, username)
        )

    elif choice == "2":
        new_phone = input("Enter new phone: ")

        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE username=%s",
            (new_phone, username)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact updated :D")

def query_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")

    rows = cur.fetchall()

    print("\nAll contacts:")

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def query_by_name():
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def query_by_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete_by_username():
    username = input("Enter username to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE username=%s",
        (username,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted :(")

def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE phone=%s",
        (phone,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted :(")

def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create table")
        print("2 - Import from CSV")
        print("3 - Add from console")
        print("4 - Update contact")
        print("5 - Show all contacts")
        print("6 - Search by name")
        print("7 - Search by phone prefix")
        print("8 - Delete by username")
        print("9 - Delete by phone")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_all()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_prefix()
        elif choice == "8":
            delete_by_username()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            print("See U next time!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()