"""Στάδιο 1 — Προσθέτω ένα παιχνίδι.

Το πρόγραμμα προσθέτει το παιχνίδι «Mini Golf» στον πίνακα games και εμφανίζει το id που του έδωσε η βάση.

ΠΡΟΣΟΧΗ: κάθε φορά που το τρέχεις προστίθεται ΝΕΑ εγγραφή. Τρέξε το μία φορά. Στο φύλλο εργασίας θα δεις τι
γίνεται όταν το τρέχεις πολλές, και πώς το καθαρίζεις στο επόμενο μάθημα.

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

# TODO 1: τα τέσσερα σημεία όπου θα μπουν οι τιμές: %s, %s, %s, %s (χωρίς εισαγωγικά γύρω τους)
sql = "INSERT INTO games (title, genre, release_year, price) VALUES (____)"

# Οι τιμές, με τη σειρά των στηλών του INSERT: title, genre, release_year, price
game = ("Mini Golf", "Αθλητικό", 2024, Decimal("3.49"))

# TODO 2: στείλε το ερώτημα μαζί με τις τιμές (δεύτερο όρισμα της execute)
cursor.execute(sql, ____)

# TODO 3: η αλλαγή δεν είναι μόνιμη αν δεν την επιβεβαιώσεις (μέθοδος της σύνδεσης)
connection.____()

# TODO 4: το id που έδωσε η βάση στη νέα εγγραφή (ιδιότητα του κέρσορα)
print(f"Προστέθηκε το «{game[0]}» με id {cursor.____}.")

cursor.close()
connection.close()
