import sqlite3
conn = sqlite3.connect('Grocery.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Grocery (data TEXT, amount real)''')
while True:
    x = int(input("Grocery List:\n1. Add an item\n2. Remove an item\n3. View the list\n4. Exit\nEnter choice: "))
    if x == 1 : 
        y = input("enter iteme ")
        z =  input("enter amount ")
        cursor.execute('INSERT INTO Grocery (data,amount) VALUES (?,?)', (y,z))
    elif x == 2:
        y = input("enter iteme ")
        cursor.execute('''DELETE FROM Grocery WHERE data == (?)''',(y,))
    elif x == 3:
        cursor.execute("SELECT * FROM Grocery")
        print(cursor.fetchall()) 
    else: 
        conn.commit()
        break
conn.close