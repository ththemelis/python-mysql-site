"""Στάδιο 4 — Η DELETE χωρίς WHERE και το δίχτυ ασφαλείας του rollback.

Το πρόγραμμα σβήνει ΟΛΕΣ τις γραμμές του games, βλέπει τι έγινε, και τις ξαναφέρνει με rollback.
Δεν έχει commit πουθενά, άρα δεν θα σβήσει τίποτα μόνιμα. ΜΗΝ προσθέσεις commit.

Συμπλήρωσε τα δύο κενά (____).
"""

import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="", database="game_library")
cursor = connection.cursor()


def count_games(cursor):
    """Επιστρέφει πόσα παιχνίδια έχει ο πίνακας games, όπως τα βλέπει αυτή η σύνδεση."""
    cursor.execute("SELECT COUNT(*) FROM games")
    return cursor.fetchone()[0]


print("Πριν από τη DELETE:", count_games(cursor), "παιχνίδια")

cursor.execute("DELETE FROM games")          # ΧΩΡΙΣ WHERE: αφορά ΟΛΕΣ τις γραμμές!

# TODO 1: πόσες γραμμές επηρέασε η DELETE; (ιδιότητα του κέρσορα)
print("Η DELETE επηρέασε", cursor.____, "γραμμές")
print("Η σύνδεσή μου βλέπει τώρα:", count_games(cursor), "παιχνίδια")

print()
input("Άνοιξε το phpMyAdmin, δες τον games (Browse) και ΜΗΝ αλλάξεις τίποτα. Μετά πάτα Enter. ")

# TODO 2: ακύρωσε την DELETE (μέθοδος της σύνδεσης)
connection.____()

print("Μετά το rollback:", count_games(cursor), "παιχνίδια")

cursor.close()
connection.close()
