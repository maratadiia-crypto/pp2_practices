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

def upsert_user():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_user(%s, %s)", (username, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("User inserted/updated!")

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

def search_pattern():
    pattern = input("Enter search pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete_user():
    value = input("Enter username or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create table")
        print("2 - Import from CSV")
        print("3 - Upsert user")
        print("4 - Show all contacts")
        print("5 - Search by name")
        print("6 - Search by phone prefix")
        print("7 - Search pattern")
        print("8 - Pagination")
        print("9 - Delete user")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            upsert_user()
        elif choice == "4":
            query_all()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_prefix()
        elif choice == "7":
            search_pattern()
        elif choice == "8":
            pagination()
        elif choice == "9":
            delete_user()
        elif choice == "0":
            print("See U next time!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()