"""Στάδιο 2 — Ο χρήστης δίνει το παιχνίδι.

Το πρόγραμμα ρωτά τον χρήστη τα στοιχεία ενός παιχνιδιού και το προσθέτει στη βάση.

ΠΡΟΣΟΧΗ: το πρόγραμμα δεν ελέγχει τι πληκτρολογείς. Αν γράψεις γράμματα στη χρονιά ή στην τιμή, θα σταματήσει με
σφάλμα. Στο Μάθημα 8 θα μάθεις να το προστατεύεις. Προς το παρόν, γράφε σωστές τιμές.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

title = input("Τίτλος: ")
genre = input("Είδος: ")

# TODO 1: η input επιστρέφει πάντα κείμενο. Μετάτρεψε τη χρονιά σε ακέραιο
year = ____(input("Χρονιά: "))

# TODO 2: μετάτρεψε την τιμή σε Decimal (από κείμενο)
price = ____(input("Τιμή: "))

sql = "INSERT INTO games (title, genre, release_year, price) VALUES (%s, %s, %s, %s)"

# TODO 3: οι τιμές σε πλειάδα, με τη σειρά των στηλών: title, genre, release_year, price
cursor.execute(sql, ____)

# TODO 4: κάνε μόνιμη την αλλαγή
connection.____()

print(f"Προστέθηκε το «{title}» με id {cursor.lastrowid}.")

cursor.close()
connection.close()
