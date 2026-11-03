"""Στάδιο 5 — Σβήνω ένα παιχνίδι με επιβεβαίωση.

Το πρόγραμμα εμφανίζει τα παιχνίδια, ρωτά ποιο id θα σβηστεί, δείχνει τον τίτλο και ζητά επιβεβαίωση. Σβήνει
μόνο αν ο χρήστης γράψει ακριβώς «ναι» και η DELETE επηρεάσει ακριβώς μία γραμμή. Στο τέλος εμφανίζει ξανά τα
παιχνίδια.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"

LIST_SQL = "SELECT id, title, genre, release_year, price FROM games ORDER BY id"


def show(cursor, title, sql):
    """Στέλνει το ερώτημα sql και εμφανίζει το αποτέλεσμα κάτω από τον τίτλο title."""
    cursor.execute(sql)
    rows = cursor.fetchall()

    print()
    print(title)
    print("-" * len(title))
    print(" | ".join(cursor.column_names))
    for row in rows:
        texts = []
        for value in row:
            texts.append(str(value))
        print(" | ".join(texts))
    print(f"Γραμμές: {len(rows)}")


connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

show(cursor, "Όλα τα παιχνίδια", LIST_SQL)
print()

game_id = int(input("id παιχνιδιού που θα σβηστεί (0 για έξοδο): "))

if game_id != 0:
    cursor.execute("SELECT title FROM games WHERE id = %s", (game_id,))
    row = cursor.fetchone()

    # TODO 1: το fetchone() δίνει None όταν δεν βρέθηκε γραμμή
    if row is ____:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
    else:
        answer = input(f"Να σβηστεί το «{row[0]}»; (ναι/όχι): ")

        if answer == "ναι":
            # TODO 2: η παράμετρος της DELETE είναι το id που έδωσε ο χρήστης (πλειάδα με μία τιμή)
            cursor.execute("DELETE FROM games WHERE id = %s", (____,))

            if cursor.rowcount == 1:
                # TODO 3: σβήστηκε ακριβώς μία γραμμή, όπως περιμέναμε: κάνε το μόνιμο
                connection.____()
                print("Το παιχνίδι σβήστηκε.")
            else:
                # TODO 4: κάτι δεν πήγε όπως περιμέναμε: ακύρωσε την αλλαγή
                connection.____()
                print("Κάτι πήγε στραβά. Δεν άλλαξε τίποτα.")
        else:
            print("Ακυρώθηκε. Δεν σβήστηκε τίποτα.")

show(cursor, "Όλα τα παιχνίδια", LIST_SQL)

cursor.close()
connection.close()
