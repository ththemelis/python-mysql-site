"""Πρόκληση 1: δύο συνδέσεις, απομόνωση και κλείδωμα. Δεν χρειάζεται να το συμπληρώσεις.

Η σύνδεση Α αλλάζει μια γραμμή ΧΩΡΙΣ commit. Δες τι βλέπει η σύνδεση Β και τι γίνεται όταν η Β προσπαθεί να αλλάξει την ΙΔΙΑ γραμμή.
"""

import time

import mysql.connector

import db
import lab_data


def copies(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT copies_available FROM games WHERE id = 1")
        return cursor.fetchone()[0]


a = db.connect()
b = db.connect()
lab_data.reset(a)
b.rollback()

print("Το Star Dodger (id 1) έχει 1 διαθέσιμο αντίτυπο. Η Β το διαβάζει: ", copies(b))
print()
print("Η Α μειώνει τα αντίτυπα του Star Dodger σε 0, ΧΩΡΙΣ commit.")
with a.cursor() as cursor:
    cursor.execute("UPDATE games SET copies_available = 0 WHERE id = 1")
print("  Η Α βλέπει:", copies(a))
print("  Η Β βλέπει:", copies(b), "  <- η αλλαγή της Α δεν έχει οριστικοποιηθεί, η Β δεν τη βλέπει")

print()
print("Η Α κάνει COMMIT.")
a.commit()
print("  Η Β βλέπει:", copies(b), "  <- η Β έχει ακόμη την ίδια «φωτογραφία» της συναλλαγής της (Μάθημα 7)")
b.rollback()
print("Η Β τελειώνει τη δική της συναλλαγή (rollback) και ξαναδιαβάζει.")
print("  Η Β βλέπει:", copies(b))

print()
print("--- Κλείδωμα ---")
print("Η Α αλλάζει ξανά το Star Dodger, ΧΩΡΙΣ commit. Η Β προσπαθεί να αλλάξει την ΙΔΙΑ γραμμή (θα περιμένει 3 δευτερόλεπτα)...")
with a.cursor() as cursor:
    cursor.execute("UPDATE games SET copies_available = 1 WHERE id = 1")
with b.cursor() as cursor:
    cursor.execute("SET SESSION innodb_lock_wait_timeout = 3")
    started = time.time()
    try:
        cursor.execute("UPDATE games SET copies_available = 2 WHERE id = 1")
        print("  Η Β τα κατάφερε.")
    except mysql.connector.Error as error:
        print(f"  Η Β περίμενε {time.time() - started:.0f} δευτ. και πήρε σφάλμα #{error.errno}: {error.msg}")

print("Η Α κάνει rollback (αφήνει τη γραμμή ελεύθερη). Η Β ξαναδοκιμάζει...")
a.rollback()
b.rollback()
with b.cursor() as cursor:
    cursor.execute("UPDATE games SET copies_available = 1 WHERE id = 1")
print("  Η Β τα κατάφερε.")
b.commit()

lab_data.reset(a)
a.close()
b.close()
