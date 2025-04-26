import psycopg2

# Соединение
conn = psycopg2.connect(
    dbname="postgres", user="postgres", password="tungtungsahur", host="localhost", port="5432"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)
    conn.commit()

def search_by_pattern():
    pattern = input("Enter search pattern (name or phone part): ")
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def insert_or_update_user():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (username, phone))
    conn.commit()
    print("User inserted or updated.")

def insert_many_users():
    n = int(input("How many users to insert? "))
    names = []
    phones = []
    for _ in range(n):
        username = input("Enter username: ")
        phone = input("Enter phone: ")
        names.append(username)
        phones.append(phone)
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    incorrect = cur.fetchone()
    if incorrect and incorrect[0]:
        print("Incorrect data:")
        print(incorrect[0])
    else:
        print("All users inserted correctly.")
    conn.commit()

def get_paginated():
    limit = int(input("Enter limit (number of rows): "))
    offset = int(input("Enter offset (how many rows to skip): "))
    cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user():
    name_or_phone = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_user_by_name_or_phone(%s)", (name_or_phone,))
    conn.commit()
    print("User deleted if existed.")

def main():
    create_table()
    while True:
        print("\n1: Search by pattern\n2: Insert or Update one user\n3: Insert many users\n4: Paginated query\n5: Delete user\n6: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            search_by_pattern()
        elif choice == "2":
            insert_or_update_user()
        elif choice == "3":
            insert_many_users()
        elif choice == "4":
            get_paginated()
        elif choice == "5":
            delete_user()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
