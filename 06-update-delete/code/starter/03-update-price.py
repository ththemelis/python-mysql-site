"""Στάδιο 2 — Αλλάζω την τιμή ενός παιχνιδιού από την Python.

Το πρόγραμμα ρωτά το id ενός παιχνιδιού και τη νέα τιμή του, και τη γράφει στη βάση.

Συμπλήρωσε τα πέντε κενά (____).
"""

from decimal import Decimal

import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="", database="game_library")
cursor = connection.cursor()

game_id = int(input("id του παιχνιδιού: "))
price = Decimal(input("Νέα τιμή: "))

# TODO 1: στη θέση της τιμής και του id βάλε σημεία παραμέτρων (χωρίς εισαγωγικά)
sql = "UPDATE games SET price = ____ WHERE id = ____"

# TODO 2: δώσε τις τιμές με τη σειρά που εμφανίζονται τα σημεία στην εντολή: πρώτα η τιμή, μετά το id
cursor.execute(sql, (____, ____))

# TODO 3: κάνε μόνιμη την αλλαγή (μέθοδος της σύνδεσης)
connection.____()

if cursor.rowcount == 0:
    print("Δεν άλλαξε καμία γραμμή: ή δεν υπάρχει τέτοιο id ή η τιμή ήταν ήδη αυτή.")
else:
    print(f"Η τιμή του παιχνιδιού με id {game_id} έγινε {price} €.")

cursor.close()
connection.close()
