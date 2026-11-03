"""Έλεγχος σύνδεσης Python → MySQL.

Τρέξε αυτό το αρχείο όταν η σύνδεση δεν δουλεύει. Δεν χρειάζεται να το συμπληρώσεις και δεν χρειάζεται (ακόμη)
να καταλάβεις τον κώδικά του: δοκιμάζει τη σύνδεση και σου λέει με απλά λόγια τι να κάνεις.
Το try/except που βλέπεις θα το μάθεις στο Μάθημα 8.

Αν τα στοιχεία σύνδεσης στον δικό σου υπολογιστή είναι διαφορετικά, άλλαξε τα HOST, PORT, USER, PASSWORD, DATABASE.
"""

import mysql.connector

HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

print(f"Δοκιμή σύνδεσης: χρήστης «{USER}» στον {HOST}:{PORT}, βάση «{DATABASE}»")

try:
    connection = mysql.connector.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
except mysql.connector.Error as error:
    print()
    print("ΑΠΟΤΥΧΙΑ:", error)
    print()
    if error.errno == 2003:
        print("Η MySQL δεν τρέχει (ή ακούει σε άλλη θύρα).")
        print("→ Άνοιξε το XAMPP Control Panel και πάτα Start στη γραμμή της MySQL.")
    elif error.errno == 1049:
        print(f"Δεν υπάρχει βάση με όνομα «{DATABASE}».")
        print("→ Δες στο phpMyAdmin πώς ακριβώς λέγεται η βάση σου και διόρθωσε το DATABASE.")
    elif error.errno == 1045:
        print("Λάθος χρήστης ή κωδικός.")
        print("→ Στο XAMPP ο χρήστης root δεν έχει κωδικό: PASSWORD = \"\".")
    elif error.errno == 2005:
        print("Λάθος όνομα εξυπηρετητή.")
        print("→ Συνήθως είναι localhost.")
    else:
        print("→ Άγνωστο σφάλμα. Δείξε το μήνυμα ΑΠΟΤΥΧΙΑ στον εκπαιδευτικό.")
else:
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    print()
    print("Η σύνδεση δουλεύει.")
    print("Πίνακες της βάσης:", ", ".join(tables))
    cursor.close()
    connection.close()
