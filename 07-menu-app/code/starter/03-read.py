"""Στάδιο 2 — Εμφανίζω και ψάχνω παιχνίδια.

Οι επιλογές 1 και 2 του μενού δουλεύουν πια: η list_games εμφανίζει όλα τα παιχνίδια και η search_games ψάχνει
με LIKE. Και οι δύο εμφανίζουν το αποτέλεσμα με την ίδια συνάρτηση, την print_games. Οι υπόλοιπες επιλογές
είναι ακόμη προσωρινές συναρτήσεις.

Συμπλήρωσε τα τρία κενά (____).
"""

import mysql.connector


def connect():
    """Ανοίγει τη σύνδεση με τη βάση game_library και την επιστρέφει."""
    return mysql.connector.connect(host="localhost", user="root", password="", database="game_library")


def show_menu():
    """Εμφανίζει το μενού επιλογών."""
    print()
    print("=== ΒΙΒΛΙΟΘΗΚΗ ΠΑΙΧΝΙΔΙΩΝ ===")
    print("1. Εμφάνιση όλων των παιχνιδιών")
    print("2. Αναζήτηση με τίτλο")
    print("3. Προσθήκη παιχνιδιού")
    print("4. Αλλαγή τιμής")
    print("5. Διαγραφή παιχνιδιού")
    print("0. Έξοδος")


def print_games(rows):
    """Εμφανίζει σε στήλες τα παιχνίδια της λίστας rows (κάθε στοιχείο είναι μια πλειάδα από το SELECT)."""
    print()
    print(f"{'id':>3}  {'Τίτλος':<20} {'Είδος':<14} {'Χρονιά':>6} {'Τιμή':>9}")
    for game_id, title, genre, year, price in rows:
        print(f"{game_id:>3}  {title:<20} {genre:<14} {year:>6} {price:>7.2f} €")
    print(f"Γραμμές: {len(rows)}")


def list_games(connection):
    """Εμφανίζει όλα τα παιχνίδια."""
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, genre, release_year, price FROM games ORDER BY id")
    # TODO 1: φέρε όλες τις γραμμές του αποτελέσματος
    rows = cursor.____()
    cursor.close()
    # TODO 2: εμφάνισε τις γραμμές με τη συνάρτηση print_games
    ____(rows)


def search_games(connection):
    """Ζητά μέρος του τίτλου και εμφανίζει τα παιχνίδια που τον περιέχουν."""
    text = input("Μέρος του τίτλου: ")
    pattern = "%" + text + "%"

    cursor = connection.cursor()
    # TODO 3: το μοτίβο του LIKE δίνεται ως παράμετρος (πλειάδα με μία τιμή)
    cursor.execute(
        "SELECT id, title, genre, release_year, price FROM games WHERE title LIKE %s ORDER BY id",
        (____,),
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        print("Δεν βρέθηκε κανένα παιχνίδι.")
    else:
        print_games(rows)


def add_game(connection):
    """Ζητά τα στοιχεία ενός παιχνιδιού και το προσθέτει στη βάση."""
    print("(Η προσθήκη θα φτιαχτεί στο Στάδιο 3.)")


def change_price(connection):
    """Ζητά το id ενός παιχνιδιού και τη νέα τιμή του, και αλλάζει την τιμή."""
    print("(Η αλλαγή τιμής θα φτιαχτεί στο Στάδιο 3.)")


def delete_game(connection):
    """Ζητά ένα id, δείχνει τον τίτλο, ζητά επιβεβαίωση και σβήνει το παιχνίδι."""
    print("(Η διαγραφή θα φτιαχτεί στο Στάδιο 4.)")


def main():
    """Το κύριο πρόγραμμα: ανοίγει τη σύνδεση και τρέχει το μενού ώσπου ο χρήστης να διαλέξει έξοδο."""
    connection = connect()

    while True:
        # Τελειώνει κάθε ανοιχτή συναλλαγή, ώστε η εφαρμογή να βλέπει τα τελευταία δεδομένα της βάσης (ενότητα 1.2)
        connection.commit()
        show_menu()
        choice = input("Επιλογή: ")

        if choice == "1":
            list_games(connection)
        elif choice == "2":
            search_games(connection)
        elif choice == "3":
            add_game(connection)
        elif choice == "4":
            change_price(connection)
        elif choice == "5":
            delete_game(connection)
        elif choice == "0":
            break
        else:
            print("Άγνωστη επιλογή. Γράψε έναν από τους αριθμούς του μενού.")

    connection.close()
    print("Γεια σου!")


main()
