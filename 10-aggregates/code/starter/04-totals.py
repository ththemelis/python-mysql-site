"""Στάδιο 3 — Συγκεντρωτικά αποτελέσματα από την Python: μια γραμμή αποτελέσματος.

Οι συναρτήσεις COUNT, SUM, AVG, MIN, MAX δίνουν ΜΙΑ γραμμή. Την παίρνεις με fetchone() και την αναλύεις σε
μεταβλητές. Η SUM και η AVG δίνουν Decimal, και αν δεν υπάρχει καμία γραμμή η AVG δίνει NULL, δηλαδή None.

Συμπλήρωσε τα πέντε κενά (____).
"""

import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="", database="game_library")
cursor = connection.cursor()

# --- 1. Τα συνολικά στοιχεία της βιβλιοθήκης -------------------------------------------------------------------
cursor.execute("SELECT COUNT(*), SUM(price), AVG(price), MIN(price), MAX(price) FROM games")
# TODO 1: το αποτέλεσμα είναι ΜΙΑ γραμμή: τη φέρνει η fetchone()
row = cursor.____()
# TODO 2: ανάλυση της πλειάδας σε πέντε μεταβλητές, με τη σειρά των στηλών
count, total, average, cheapest, dearest = ____

print(f"Παιχνίδια: {count}")
print(f"Συνολική αξία: {total:.2f} €")
print(f"Μέση τιμή: {average:.2f} €")
print(f"Φθηνότερο: {cheapest:.2f} €  |  Ακριβότερο: {dearest:.2f} €")
print()

# --- 2. Τα στοιχεία ενός είδους, της επιλογής του χρήστη ---------------------------------------------------------
genre = input("Είδος: ")
cursor.execute("SELECT COUNT(*), AVG(price) FROM games WHERE genre = %s", (genre,))
count, average = cursor.fetchone()

# TODO 3: αν δεν υπάρχει κανένα παιχνίδι, η AVG δίνει NULL, δηλαδή None στην Python
if average is ____:
    print(f"Κανένα παιχνίδι στο είδος «{genre}».")
else:
    # TODO 4: η μέση τιμή είναι Decimal με πολλά δεκαδικά· η μορφή .2f την εμφανίζει με δύο
    print(f"Το είδος «{genre}» έχει {count} παιχνίδια, με μέση τιμή {average:____} €.")
print()

# --- 3. Ποιο παιχνίδι είναι το ακριβότερο; Η MAX δίνει τιμή, όχι γραμμή ----------------------------------------------
# TODO 5: ταξινόμηση από την ακριβότερη τιμή προς τη φθηνότερη
cursor.execute("SELECT title, price FROM games ORDER BY price ____ LIMIT 1")
title, price = cursor.fetchone()
print(f"Το ακριβότερο παιχνίδι είναι το «{title}» ({price:.2f} €).")

cursor.close()
connection.close()
