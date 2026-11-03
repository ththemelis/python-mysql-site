"""Στάδιο 3 — Ο κατάλογος των παιχνιδιών.

Το πρόγραμμα διαβάζει τα παιχνίδια από τη βάση και τα εμφανίζει σε στήλες.

Συμπλήρωσε τα δύο κενά (____).
"""

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

cursor.execute("SELECT title, genre, price FROM games")
rows = cursor.fetchall()

cursor.close()
connection.close()

print("ΒΙΒΛΙΟΘΗΚΗ ΠΑΙΧΝΙΔΙΩΝ")
print("=" * 42)

# TODO 1: για κάθε γραμμή του αποτελέσματος, δώσε ονόματα στα τρία στοιχεία της: title, genre, price
for ____ in rows:
    # TODO 2: η τιμή σε 6 θέσεις, στοιχισμένη δεξιά, με 2 δεκαδικά (η μορφή που ξεκινά με >)
    print(f"{title:<18} {genre:<14} {price:____} €")

print("=" * 42)
print(f"Σύνολο: {len(rows)} παιχνίδια")
