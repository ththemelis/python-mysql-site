"""Στάδιο 1 — Το πρώτο JOIN από την Python.

Ένα ερώτημα JOIN στέλνεται από την Python όπως κάθε άλλο ερώτημα: είναι απλώς ένα κείμενο στη cursor.execute.
Δουλεύει με τη βάση όπως τη φέρνει το 01-start-state.sql. Εδώ τα αποτελέσματα διαβάζονται ως πλειάδες, όπως στα
Μαθήματα 3–10.

Συμπλήρωσε τα τρία κενά (____).
"""

import mysql.connector


def main():
    """Φέρνει όλα τα παιχνίδια μαζί με το όνομα του είδους τους και τα εμφανίζει σε στήλες."""
    connection = mysql.connector.connect(host="localhost", user="root", password="", database="game_library")
    cursor = connection.cursor()

    # TODO 1: το JOIN ενώνει τον games με τον genres (το ερώτημα είναι ένα κείμενο που σπάει σε γραμμές)
    cursor.execute(
        "SELECT g.id, g.title, ge.name, g.release_year, g.price "
        "FROM games AS g "
        "____ genres AS ge ON g.genre_id = ge.____ "
        "ORDER BY g.id"
    )
    rows = cursor.fetchall()
    cursor.close()

    print(f"{'id':>3}  {'Τίτλος':<20} {'Είδος':<14} {'Χρονιά':>6} {'Τιμή':>9}")
    # Οι πέντε μεταβλητές παίρνουν τις τιμές με τη σειρά των στηλών του SELECT
    for game_id, title, genre_name, year, price in rows:
        print(f"{game_id:>3}  {title:<20} {genre_name:<14} {year:>6} {price:>7.2f} €")
    # TODO 2: πόσες γραμμές έχει το αποτέλεσμα;
    print(f"Γραμμές: {len(____)}")

    connection.close()


main()
