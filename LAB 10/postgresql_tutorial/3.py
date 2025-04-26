import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    dbname = "postgres",
    user = "nurbol",
    password = "123nurbolik006"
)

cur = conn.cursor()

choice = input("What do you wanna update ? 'name' or 'phone' brother :) : ")

if choice == "name":
    cur_name = input("Which name ?: ")
    new_name = input("Enter your new name: ")
    cur.execute("""UPDATE phonebook set name = %s WHERE name = %s""", (new_name, cur_name))
elif choice == "phone":
    cur_phone_n = input("Which phone number?: ")
    new_phone_n = input("Enter your new phone number: ")
    cur.execute("""UPDATE phonebook set phone = %s WHERE phone = %s""", (new_phone_n, cur_phone_n))

else:
    print("There are no other options :(")


conn.commit()

cur.execute("""SELECT * FROM phonebook""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()
