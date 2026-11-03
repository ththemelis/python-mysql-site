"""Στάδιο 2 — Το πρώτο ερώτημα.

Το πρόγραμμα ζητά από τη βάση τους τίτλους και τις τιμές των παιχνιδιών και τα εμφανίζει
όπως τα επιστρέφει η Python, χωρίς καμία μορφοποίηση.

Συμπλήρωσε τα τρία κενά (____).
"""

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

# TODO 1: το ερώτημα SQL (μέσα σε εισαγωγικά) που επιστρέφει τον τίτλο και την τιμή κάθε παιχνιδιού
cursor.execute(____)

# TODO 2: φέρε ΟΛΕΣ τις γραμμές του αποτελέσματος (μέθοδος του cursor)
rows = cursor.____()

print(rows)
print("Πλήθος γραμμών:", len(rows))

# TODO 3: το πρώτο στοιχείο της λίστας rows (η πρώτη γραμμή του αποτελέσματος)
print("Πρώτη γραμμή:", ____)

cursor.close()
connection.close()
