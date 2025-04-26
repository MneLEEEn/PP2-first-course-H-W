import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    dbname = "postgres",
    user = "nurbol",
    password = "123nurbolik006"
)

cur = conn.cursor()

choice = input("BY What do you wanna delete row ? 'name' or 'phone': ")

if choice == "name":
    name = input("Enter name: ")
    cur.execute("""DELETE FROM phonebook WHERE name = %s""", (name,))
elif choice == "phone":
    phone = input("Enter phone number: ")
    cur.execute("""DELETE FROM phonebook WHERE phone = %s""", (phone,))
else:
    print("You entered wrong option, try again!")

conn.commit()

cur.execute("""SELECT * FROM phonebook""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()