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

    print("Table created successfully.")


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


def upsert_one_user():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_user(%s, %s)", (username, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("User inserted or updated successfully.")


def insert_multiple_users():
    count = int(input("How many users do you want to add? "))

    usernames = []
    phones = []

    for i in range(count):
        print(f"\nUser {i + 1}")
        username = input("Enter username: ").strip()
        phone = input("Enter phone: ").strip()

        usernames.append(username)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM insert_multiple_users(%s, %s)",
        (usernames, phones)
    )

    incorrect_rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    print("\nUsers processed.")

    if incorrect_rows:
        print("\nIncorrect data:")
        for row in incorrect_rows:
            print(row)
    else:
        print("All users were added successfully.")


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    if rows:
        print("\nAll contacts:")
        for row in rows:
            print(row)
    else:
        print("Phonebook is empty.")

    cur.close()
    conn.close()


def search_by_name():
    name = input("Enter name to search: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username ILIKE %s ORDER BY id",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    if rows:
        print("\nSearch results:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def search_by_prefix():
    prefix = input("Enter phone prefix: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id",
        (prefix + '%',)
    )

    rows = cur.fetchall()

    if rows:
        print("\nSearch results:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def search_pattern():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM phonebook
        WHERE username ILIKE %s OR phone ILIKE %s
        ORDER BY id
        """,
        ('%' + pattern + '%', '%' + pattern + '%')
    )

    rows = cur.fetchall()

    if rows:
        print("\nSearch results:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s",(limit, offset)
    )

    rows = cur.fetchall()

    if rows:
        print("\nPaginated results:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def delete_user():
    value = input("Enter username or phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted successfully.")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create table")
        print("2 - Import from CSV")
        print("3 - Upsert one user")
        print("4 - Insert multiple users")
        print("5 - Show all contacts")
        print("6 - Search by name")
        print("7 - Search by phone prefix")
        print("8 - Search pattern")
        print("9 - Pagination")
        print("10 - Delete user")
        print("0 - Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            upsert_one_user()
        elif choice == "4":
            insert_multiple_users()
        elif choice == "5":
            show_all_contacts()
        elif choice == "6":
            search_by_name()
        elif choice == "7":
            search_by_prefix()
        elif choice == "8":
            search_pattern()
        elif choice == "9":
            pagination()
        elif choice == "10":
            delete_user()
        elif choice == "0":
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()