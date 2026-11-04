"""Στάδιο 4 — Η αναφορά της βιβλιοθήκης: ομάδες και «μπάρες».

Το πρόγραμμα εμφανίζει τα συνολικά στοιχεία, τα είδη με τουλάχιστον μερικά παιχνίδια (με HAVING και παράμετρο που
ρωτά τον χρήστη) και τα παιχνίδια ανά χρονιά, με μια «μπάρα» από τετράγωνα για κάθε ομάδα.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

import mysql.connector


def connect():
    """Ανοίγει τη σύνδεση με τη βάση game_library και την επιστρέφει."""
    return mysql.connector.connect(host="localhost", user="root", password="", database="game_library")


def ask_int(message, low, high):
    """Ρωτά ώσπου ο χρήστης να γράψει ακέραιο από low έως high, και τον επιστρέφει."""
    while True:
        text = input(message)
        try:
            number = int(text)
            if low <= number <= high:
                return number
            print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")
        except ValueError:
            print("Γράψε έναν ακέραιο αριθμό.")


def show_totals(connection):
    """Εμφανίζει τα συνολικά στοιχεία της βιβλιοθήκης."""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*), SUM(price), AVG(price), MIN(price), MAX(price) FROM games")
    count, total, average, cheapest, dearest = cursor.fetchone()
    cursor.close()

    print("ΣΥΝΟΛΙΚΑ ΣΤΟΙΧΕΙΑ")
    print(f"Παιχνίδια: {count}")
    print(f"Συνολική αξία: {total:.2f} €")
    print(f"Μέση τιμή: {average:.2f} €")
    print(f"Φθηνότερο: {cheapest:.2f} €  |  Ακριβότερο: {dearest:.2f} €")


def show_by_genre(connection, min_count):
    """Εμφανίζει πόσα παιχνίδια και ποια μέση τιμή έχει κάθε είδος, για τα είδη με τουλάχιστον min_count παιχνίδια."""
    cursor = connection.cursor()
    # TODO 1: το HAVING φιλτράρει τις ΟΜΑΔΕΣ (το min_count δίνεται ως παράμετρος)
    cursor.execute(
        "SELECT genre, COUNT(*), AVG(price) FROM games GROUP BY genre "
        "____ COUNT(*) >= %s ORDER BY COUNT(*) DESC, genre",
        (min_count,),
    )
    rows = cursor.fetchall()
    cursor.close()

    print()
    print(f"ΕΙΔΗ ΜΕ ΤΟΥΛΑΧΙΣΤΟΝ {min_count} ΠΑΙΧΝΙΔΙΑ")
    if len(rows) == 0:
        print("Κανένα είδος δεν έχει τόσα παιχνίδια.")
        return

    # TODO 2: κάθε στοιχείο της λίστας είναι μια γραμμή αποτελέσματος (genre, n, average)
    for genre, n, average in ____:
        # TODO 3: μια «μπάρα» από n τετράγωνα (ένα κείμενο επαναλαμβάνεται με το *)
        bar = "█" * ____
        print(f"{genre:<12} {bar:<6} {n:>2}   {average:>6.2f} €")


def show_by_year(connection):
    """Εμφανίζει πόσα παιχνίδια κυκλοφόρησαν κάθε χρονιά."""
    cursor = connection.cursor()
    # TODO 4: ομάδες ανά χρονιά κυκλοφορίας: GROUP BY
    cursor.execute("SELECT release_year, COUNT(*) FROM games ____ BY release_year ORDER BY release_year")
    rows = cursor.fetchall()
    cursor.close()

    print()
    print("ΠΑΙΧΝΙΔΙΑ ΑΝΑ ΧΡΟΝΙΑ ΚΥΚΛΟΦΟΡΙΑΣ")
    for year, n in rows:
        print(f"{year}  {'█' * n:<7} {n}")


def main():
    """Το κύριο πρόγραμμα: εμφανίζει την αναφορά της βιβλιοθήκης."""
    connection = connect()

    show_totals(connection)
    print()
    min_count = ask_int("Εμφάνιση ειδών με τουλάχιστον πόσα παιχνίδια; ", 1, 100)
    show_by_genre(connection, min_count)
    show_by_year(connection)

    connection.close()


main()
