"""Στάδιο 3 — Γιατί όχι f-strings στη SQL.

Το πρόγραμμα ψάχνει παιχνίδια με τίτλο ΙΣΟ με αυτό που πληκτρολογείς, με δύο τρόπους:

  1. ΑΣΦΑΛΗΣ:     στέλνει το κείμενο ως παράμετρο (%s).
  2. ΕΠΙΚΙΝΔΥΝΟΣ: βάζει το κείμενο μέσα στη SQL με f-string.

Δεν υπάρχουν κενά να συμπληρώσεις. Τρέξε το ΤΡΕΙΣ φορές, με αυτές τις εισόδους, και σύγκρινε τους δύο τρόπους:

    Είσοδος 1:   Neon Soccer
    Είσοδος 2:   Tom's Quest
    Είσοδος 3:   x' OR '1'='1

Πρόβλεψε πρώτα τι θα συμβεί σε κάθε περίπτωση.
Ο δεύτερος τρόπος ΔΕΝ πρέπει να χρησιμοποιείται σε πραγματικά προγράμματα.
"""

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

text = input("Τίτλος παιχνιδιού: ")

print()
print("--- 1. Ασφαλής τρόπος: παράμετρος %s ---")
cursor.execute("SELECT title, price FROM games WHERE title = %s", (text,))
rows = cursor.fetchall()
print(f"Βρέθηκαν {len(rows)} γραμμές.")
for title, price in rows[:3]:
    print(f"  {title}  {price}")

print()
print("--- 2. Επικίνδυνος τρόπος: f-string ---")
sql = f"SELECT title, price FROM games WHERE title = '{text}'"
print("Το ερώτημα που στάλθηκε:")
print("  " + sql)
cursor.execute(sql)
rows = cursor.fetchall()
print(f"Βρέθηκαν {len(rows)} γραμμές.")
for title, price in rows[:3]:
    print(f"  {title}  {price}")

cursor.close()
connection.close()
