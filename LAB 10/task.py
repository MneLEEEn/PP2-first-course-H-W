import psycopg2
import csv

# Connect to PostgreSQL
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
        )
    """)
    conn.commit()

def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("Data inserted from CSV.")

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Data inserted from console.")

def update_user():
    id_to_update = input("Enter ID to update: ")
    choice = input("Update (1) username or (2) phone? ")
    if choice == "1":
        new_username = input("Enter new username: ")
        cur.execute("UPDATE PhoneBook SET username = %s WHERE id = %s", (new_username, id_to_update))
    elif choice == "2":
        new_phone = input("Enter new phone: ")
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE id = %s", (new_phone, id_to_update))
    conn.commit()
    print("User updated.")

def query_data():
    print("1: All users\n2: Search by username\n3: Search by phone pattern")
    choice = input("Choose option: ")
    if choice == "1":
        cur.execute("SELECT * FROM PhoneBook")
    elif choice == "2":
        username = input("Enter username to search: ")
        cur.execute("SELECT * FROM PhoneBook WHERE username = %s", (username,))
    elif choice == "3":
        pattern = input("Enter phone pattern (e.g., %123%): ")
        cur.execute("SELECT * FROM PhoneBook WHERE phone LIKE %s", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user():
    choice = input("Delete by (1) username or (2) phone? ")
    if choice == "1":
        username = input("Enter username: ")
        cur.execute("DELETE FROM PhoneBook WHERE username = %s", (username,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
    conn.commit()
    print("User deleted.")

def main():
    create_table()
    while True:
        print("\n1: Insert from CSV\n2: Insert from Console\n3: Update User\n4: Query Data\n5: Delete User\n6: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            insert_from_csv('phonebook.csv')
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_user()
        elif choice == "4":
            query_data()
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
