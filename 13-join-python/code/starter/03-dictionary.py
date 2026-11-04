"""Στάδιο 2 — Τα αποτελέσματα ως λεξικά (dictionary=True).

Τα αποτελέσματα ενός JOIN έχουν πολλές στήλες. Με dictionary=True κάθε γραμμή γίνεται λεξικό και τη διαβάζεις με το
ΟΝΟΜΑ της στήλης (row["title"]), όχι με τη θέση της. Το ψευδώνυμο AS της SQL είναι το κλειδί του λεξικού.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

import mysql.connector


def connect():
    """Ανοίγει τη σύνδεση με τη βάση game_library και την επιστρέφει."""
    return mysql.connector.connect(host="localhost", user="root", password="", database="game_library")


def print_games(rows):
    """Εμφανίζει σε στήλες τα παιχνίδια της λίστας rows (κάθε στοιχείο είναι ένα λεξικό από το SELECT)."""
    print()
    print(f"{'id':>3}  {'Τίτλος':<20} {'Είδος':<14} {'Χρονιά':>6} {'Τιμή':>9}  {'Προστέθηκε':<10}")
    for row in rows:
        added = row["added_on"].strftime("%d/%m/%Y")
        # TODO 1: το κλειδί του λεξικού είναι το όνομα (ή το ψευδώνυμο) της στήλης στο SELECT
        print(f"{row['id']:>3}  {row['title']:<20} {row['____']:<14} {row['release_year']:>6} {row['price']:>7.2f} €  {added:<10}")
    print(f"Γραμμές: {len(rows)}")


def list_games(connection):
    """Εμφανίζει όλα τα παιχνίδια, με το όνομα του είδους τους (JOIN με τον genres)."""
    # TODO 2: με dictionary=True κάθε γραμμή του αποτελέσματος γίνεται λεξικό
    cursor = connection.cursor(dictionary=____)
    cursor.execute(
        # TODO 3: το ψευδώνυμο της στήλης γίνεται το κλειδί του λεξικού
        "SELECT g.id, g.title, ge.name AS ____, g.release_year, g.price, g.added_on "
        "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
        "ORDER BY g.id"
    )
    rows = cursor.fetchall()
    cursor.close()
    print_games(rows)


def search_games(connection):
    """Ζητά μέρος του τίτλου και εμφανίζει τα παιχνίδια που τον περιέχουν."""
    text = input("Μέρος του τίτλου: ")
    pattern = "%" + text + "%"

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.id, g.title, ge.name AS genre_name, g.release_year, g.price, g.added_on "
        "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
        "WHERE g.title LIKE %s ORDER BY g.id",
        (pattern,),
    )
    # TODO 4: η fetchall φέρνει όλες τις γραμμές ως λίστα (εδώ λίστα από λεξικά)
    rows = cursor.____()
    cursor.close()

    if len(rows) == 0:
        print("Δεν βρέθηκε κανένα παιχνίδι.")
    else:
        print_games(rows)


def id_clash(connection):
    """Πείραμα: τι γίνεται όταν δύο στήλες του αποτελέσματος έχουν το ίδιο όνομα;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT g.id, ge.id FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id WHERE g.id = 9")
    row = cursor.fetchone()
    cursor.close()

    print()
    print("Πείραμα με δύο στήλες id:", row)


def main():
    """Το κύριο πρόγραμμα: δείχνει όλα τα παιχνίδια, μία αναζήτηση και το πείραμα με το ίδιο όνομα στηλών."""
    connection = connect()

    list_games(connection)
    search_games(connection)
    id_clash(connection)

    connection.close()


main()
