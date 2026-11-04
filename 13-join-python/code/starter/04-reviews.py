"""Στάδιο 3 — Κριτικές με JOIN και LEFT JOIN από την Python.

Η show_reviews δείχνει τις κριτικές ενός παιχνιδιού με LEFT JOIN, ώστε να ξεχωρίζει το «δεν υπάρχει παιχνίδι» από το
«δεν έχει κριτικές» (στήλες NULL, δηλαδή None στην Python). Η games_without_reviews βρίσκει τα παιχνίδια χωρίς κριτική.

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


def show_reviews(connection, game_id):
    """Εμφανίζει τις κριτικές ενός παιχνιδιού. Το LEFT JOIN κρατά το παιχνίδι ακόμη κι αν δεν έχει καμία κριτική."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.title, r.stars, r.comment "
        "FROM games AS g "
        # TODO 1: LEFT JOIN: το παιχνίδι μένει στο αποτέλεσμα ακόμη κι αν δεν έχει κριτική (τότε r.stars είναι NULL)
        "____ JOIN reviews AS r ON r.game_id = g.id "
        "WHERE g.id = %s ORDER BY r.id",
        (game_id,),
    )
    rows = cursor.fetchall()
    cursor.close()

    # Καμία γραμμή: δεν υπάρχει παιχνίδι με αυτό το id
    if len(rows) == 0:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    # TODO 2: το κλειδί του τίτλου στο λεξικό της πρώτης γραμμής
    print(f"Κριτικές για το «{rows[0]['____']}»:")
    # TODO 3: το NULL της βάσης γίνεται None στην Python (έλεγχος με is, όχι με ==)
    if rows[0]["stars"] is ____:
        print("  Κανείς δεν έγραψε ακόμη κριτική.")
        return

    for row in rows:
        if row["comment"] is None:
            comment = "(χωρίς σχόλιο)"
        else:
            comment = row["comment"]
        print(f"  {'*' * row['stars']:<5}  {comment}")


def games_without_reviews(connection):
    """Εμφανίζει τα παιχνίδια που δεν έχουν καμία κριτική."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.id, g.title, g.price "
        "FROM games AS g "
        "LEFT JOIN reviews AS r ON r.game_id = g.id "
        # TODO 4: τα παιχνίδια χωρίς ταίρι στον reviews έχουν NULL στην r.id
        "WHERE r.id IS ____ "
        "ORDER BY g.title"
    )
    rows = cursor.fetchall()
    cursor.close()

    print()
    print(f"Παιχνίδια χωρίς καμία κριτική: {len(rows)}")
    for row in rows:
        print(f"{row['id']:>3}  {row['title']:<20} {row['price']:>7.2f} €")


def main():
    """Το κύριο πρόγραμμα: ρωτά ένα id και δείχνει τις κριτικές του, και μετά τα παιχνίδια χωρίς κριτική."""
    connection = connect()

    game_id = ask_int("id παιχνιδιού: ", 1, 100000)
    show_reviews(connection, game_id)
    games_without_reviews(connection)

    connection.close()


main()
