"""Στάδιο 4 — Προσθήκη παιχνιδιών σε βρόχο.

Το πρόγραμμα ζητά στοιχεία παιχνιδιών και τα προσθέτει στη βάση, ώσπου να αφήσεις κενό τον τίτλο. Στο τέλος
εμφανίζει όλα τα παιχνίδια με τη συνάρτηση show του Μαθήματος 4.

ΠΡΟΣΟΧΗ: το πρόγραμμα δεν ελέγχει τι πληκτρολογείς (έρχεται στο Μάθημα 8). Γράφε σωστές τιμές.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

INSERT_SQL = "INSERT INTO games (title, genre, release_year, price) VALUES (%s, %s, %s, %s)"


def show(cursor, title, sql):
    """Στέλνει το ερώτημα sql και εμφανίζει το αποτέλεσμα κάτω από τον τίτλο title."""
    cursor.execute(sql)
    rows = cursor.fetchall()

    print()
    print(title)
    print("-" * len(title))
    print(" | ".join(cursor.column_names))
    for row in rows:
        texts = []
        for value in row:
            texts.append(str(value))
        print(" | ".join(texts))
    print(f"Γραμμές: {len(rows)}")


connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

print("ΠΡΟΣΘΗΚΗ ΠΑΙΧΝΙΔΙΩΝ")
print("Άφησε τον τίτλο κενό και πάτα Enter για να τελειώσεις.")
print()

title = input("Τίτλος: ")

# TODO 1: συνέχισε όσο ο τίτλος ΔΕΝ είναι κενός (το κενό κείμενο γράφεται "")
while ____:
    genre = input("Είδος: ")
    year = int(input("Χρονιά: "))
    price = Decimal(input("Τιμή: "))

    # TODO 2: στείλε το INSERT_SQL με τις τιμές σε πλειάδα (title, genre, year, price)
    cursor.execute(INSERT_SQL, ____)

    # TODO 3: κάνε μόνιμη την αλλαγή (μέθοδος της σύνδεσης)
    connection.____()

    print(f"Προστέθηκε το «{title}» με id {cursor.lastrowid}.")
    print()

    # TODO 4: ρώτα ξανά για τον επόμενο τίτλο, με την ίδια εντολή που ρώτησες την πρώτη φορά
    title = ____("Τίτλος: ")

show(cursor, "Όλα τα παιχνίδια", "SELECT id, title, genre, release_year, price FROM games ORDER BY id")

cursor.close()
connection.close()
