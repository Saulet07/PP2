from connect import connect


def insert_or_update():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()

    cur.close()
    conn.close()


def search():
    pattern = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete():
    value = input("Delete by name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()

    cur.close()
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

while True:
    print("\n===== PHONEBOOK =====")
    print("1. Insert/Update")
    print("2. Search")
    print("3. Delete")
    print("4. Pagination")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        insert_or_update()
    elif choice == "2":
        search()
    elif choice == "3":
        delete()
    elif choice == "4":
        pagination()
    elif choice == "5":
        print("Goodbye")
        break
    else:
        print("Invalid choice")