"""Στάδιο 1 — Η πρώτη σύνδεση.

Το πρόγραμμα συνδέεται στη βάση game_library και εμφανίζει αν η σύνδεση δουλεύει.
Πριν το τρέξεις: ξεκίνα τη MySQL από το XAMPP Control Panel (ο Apache δεν χρειάζεται).

Συμπλήρωσε τα τέσσερα κενά (____).
"""

import mysql.connector

connection = mysql.connector.connect(
    host=____,        # TODO 1: ο υπολογιστής του εξυπηρετητή (αυτός εδώ)
    user=____,        # TODO 2: ο χρήστης του XAMPP
    password=____,    # TODO 3: ο κωδικός (ο χρήστης του XAMPP δεν έχει κωδικό)
    database=____,    # TODO 4: η βάση που φτιάξαμε
)

print("Συνδέθηκες:", connection.is_connected())

connection.close()
print("Η σύνδεση έκλεισε.")
