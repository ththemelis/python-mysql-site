"""Έλεγχος του Σταδίου 1: δοκιμάζει τα config.py και db.py. Δεν χρειάζεται να το συμπληρώσεις."""

import db

with db.connect() as connection:
    print("Μέσα στο with: η σύνδεση είναι ανοιχτή:", connection.is_connected())
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM games")
        print("Παιχνίδια στη βάση:", cursor.fetchone()[0])

print("Μετά το with: η σύνδεση είναι ανοιχτή:", connection.is_connected())
