import csv
import json
import os
from connect import connect


def run_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()

    print(filename, "executed successfully.")


def create_schema():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    username = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    birthday = input("Enter birthday YYYY-MM-DD: ").strip()
    group_name = input("Enter group: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter phone type home/work/mobile: ").strip()

    conn = connect()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username)
        DO UPDATE SET email = EXCLUDED.email,
                      birthday = EXCLUDED.birthday,
                      group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (username, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved successfully.")


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Enter email pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        ORDER BY c.id
    """, ("%" + email + "%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Enter group name: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        ORDER BY c.id
    """, ("%" + group_name + "%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_pattern():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    print("1 - Sort by name")
    print("2 - Sort by birthday")
    print("3 - Sort by date added")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        order_by = "c.username"
    elif choice == "2":
        order_by = "c.birthday"
    else:
        order_by = "c.created_at"

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {order_by}
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def pagination_loop():
    limit = int(input("Enter page size: "))
    offset = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\nPage:")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("\nnext / prev / quit: ").strip().lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command.")


def import_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute(
                """
                INSERT INTO contacts(username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username)
                DO UPDATE SET email = EXCLUDED.email,
                              birthday = EXCLUDED.birthday,
                              group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (row["username"], row["email"], row["birthday"], group_id)
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, row["phone"], row["type"])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported successfully.")


def export_to_json(filename):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phone": row[5],
            "type": row[6]
        })

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("JSON exported successfully.")


def import_from_json(filename):
    conn = connect()
    cur = conn.cursor()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        username = item["username"]

        cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            answer = input(f"{username} exists. overwrite or skip? ").strip().lower()

            if answer == "skip":
                continue

        group_id = get_group_id(cur, item["group"])

        cur.execute(
            """
            INSERT INTO contacts(username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username)
            DO UPDATE SET email = EXCLUDED.email,
                          birthday = EXCLUDED.birthday,
                          group_id = EXCLUDED.group_id
            RETURNING id
            """,
            (username, item["email"], item["birthday"], group_id)
        )

        contact_id = cur.fetchone()[0]

        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

        cur.execute(
            "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, item["phone"], item["type"])
        )

    conn.commit()
    cur.close()
    conn.close()

    print("JSON imported successfully.")


def add_phone_to_contact():
    name = input("Enter contact name: ").strip()
    phone = input("Enter new phone: ").strip()
    phone_type = input("Enter phone type home/work/mobile: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_contact_to_group():
    name = input("Enter contact name: ").strip()
    group_name = input("Enter new group: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create schema")
        print("2 - Add contact")
        print("3 - Show all contacts")
        print("4 - Search by email")
        print("5 - Filter by group")
        print("6 - Search pattern")
        print("7 - Sort contacts")
        print("8 - Pagination")
        print("9 - Import from CSV")
        print("10 - Export to JSON")
        print("11 - Import from JSON")
        print("12 - Add phone")
        print("13 - Move to group")
        print("0 - Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_schema()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            show_all_contacts()
        elif choice == "4":
            search_by_email()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            search_pattern()
        elif choice == "7":
            sort_contacts()
        elif choice == "8":
            pagination_loop()
        elif choice == "9":
            import_from_csv("contacts.csv")
        elif choice == "10":
            export_to_json("contacts.json")
        elif choice == "11":
            import_from_json("contacts.json")
        elif choice == "12":
            add_phone_to_contact()
        elif choice == "13":
            move_contact_to_group()
        elif choice == "0":
            print("See you next time!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()