"""Στάδιο 4 — Ο κατάλογος με σύνολα.

Το πρόγραμμα εμφανίζει τις πλατφόρμες και τα παιχνίδια και υπολογίζει στην Python το σύνολο, τον μέσο
όρο και το σύνολο με ΦΠΑ.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

# ΦΠΑ 24%. Είναι Decimal και όχι 1.24, γιατί οι τιμές που επιστρέφει η βάση (DECIMAL) είναι Decimal.
VAT = Decimal("1.24")

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

cursor.execute("SELECT name, maker, release_year FROM platforms")
platforms = cursor.fetchall()

cursor.execute("SELECT title, genre, price FROM games")
games = cursor.fetchall()

# Τα δεδομένα βρίσκονται πλέον στις λίστες platforms και games. Η σύνδεση δεν χρειάζεται άλλο.
cursor.close()
connection.close()

print("ΠΛΑΤΦΟΡΜΕΣ")
# TODO 1: για κάθε πλατφόρμα, δώσε ονόματα στα τρία στοιχεία της: name, maker, year
for ____ in platforms:
    print(f"- {name} ({maker}, {year})")

print()
print("ΠΑΙΧΝΙΔΙΑ")
total = 0
for title, genre, price in games:
    print(f"{title:<18} {genre:<14} {price:>6.2f} €")
    # TODO 2: πρόσθεσε την τιμή του παιχνιδιού στο άθροισμα total
    total = total + ____

# TODO 3: ο μέσος όρος: το άθροισμα διά το πλήθος των παιχνιδιών (len της λίστας games)
average = total / ____

print("-" * 42)
print(f"Πλήθος παιχνιδιών: {len(games)}")
print(f"Συνολική αξία:     {total:.2f} €")
print(f"Μέση τιμή:         {average:.2f} €")
# TODO 4: το σύνολο με ΦΠΑ: πολλαπλασίασε το σύνολο με τη σταθερά VAT
print(f"Σύνολο με ΦΠΑ:     {____:.2f} €")
