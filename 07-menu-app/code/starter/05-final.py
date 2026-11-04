"""Στάδιο 4 — Η ολοκληρωμένη εφαρμογή: διαγραφή με επιβεβαίωση.

Η επιλογή 5 δουλεύει πια. Η delete_game ζητά από τη find_title τον τίτλο του παιχνιδιού (η find_title ΕΠΙΣΤΡΕΦΕΙ
τον τίτλο ή None), ρωτά τον χρήστη, και σβήνει μόνο αν γράψει ακριβώς «ναι».

ΠΡΟΣΟΧΗ: το πρόγραμμα δεν ελέγχει τι πληκτρολογείς (έρχεται στο Μάθημα 8). Γράφε σωστές τιμές.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal

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
    rows = cursor.fetchall()
    cursor.close()
    print_games(rows)


def search_games(connection):
    """Ζητά μέρος του τίτλου και εμφανίζει τα παιχνίδια που τον περιέχουν."""
    text = input("Μέρος του τίτλου: ")
    pattern = "%" + text + "%"

    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, title, genre, release_year, price FROM games WHERE title LIKE %s ORDER BY id",
        (pattern,),
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        print("Δεν βρέθηκε κανένα παιχνίδι.")
    else:
        print_games(rows)


def add_game(connection):
    """Ζητά τα στοιχεία ενός παιχνιδιού και το προσθέτει στη βάση."""
    title = input("Τίτλος: ")
    genre = input("Είδος: ")
    year = int(input("Χρονιά: "))
    price = Decimal(input("Τιμή: "))

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO games (title, genre, release_year, price) VALUES (%s, %s, %s, %s)",
        (title, genre, year, price),
    )
    connection.commit()
    print(f"Προστέθηκε το «{title}» με id {cursor.lastrowid}.")
    cursor.close()


def change_price(connection):
    """Ζητά το id ενός παιχνιδιού και τη νέα τιμή του, και αλλάζει την τιμή."""
    game_id = int(input("id παιχνιδιού: "))
    price = Decimal(input("Νέα τιμή: "))

    cursor = connection.cursor()
    cursor.execute("UPDATE games SET price = %s WHERE id = %s", (price, game_id))
    connection.commit()

    if cursor.rowcount == 0:
        print("Δεν άλλαξε καμία γραμμή: ή δεν υπάρχει τέτοιο id ή η τιμή ήταν ήδη αυτή.")
    else:
        print(f"Η τιμή του παιχνιδιού με id {game_id} έγινε {price} €.")
    cursor.close()


def find_title(connection, game_id):
    """Επιστρέφει τον τίτλο του παιχνιδιού με το id που δόθηκε, ή None αν δεν υπάρχει τέτοιο παιχνίδι."""
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM games WHERE id = %s", (game_id,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        # TODO 1: επίστρεψε None, γιατί δεν βρέθηκε γραμμή
        ____ None
    return row[0]


def delete_game(connection):
    """Ζητά ένα id, δείχνει τον τίτλο, ζητά επιβεβαίωση και σβήνει το παιχνίδι."""
    game_id = int(input("id παιχνιδιού που θα σβηστεί: "))

    # TODO 2: ρώτα τη find_title για τον τίτλο (δίνεις τη σύνδεση και το id)
    title = ____(connection, game_id)
    if title is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    answer = input(f"Να σβηστεί το «{title}»; (ναι/όχι): ")
    # TODO 3: μόνο το ακριβές «ναι» σβήνει: ό,τι είναι διαφορετικό ακυρώνει
    if answer ____ "ναι":
        print("Ακυρώθηκε. Δεν σβήστηκε τίποτα.")
        return

    cursor = connection.cursor()
    cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
    if cursor.rowcount == 1:
        connection.commit()
        print("Το παιχνίδι σβήστηκε.")
    else:
        # TODO 4: κάτι δεν πήγε όπως περιμέναμε: ακύρωσε την αλλαγή (μέθοδος της σύνδεσης)
        connection.____()
        print("Κάτι πήγε στραβά. Δεν άλλαξε τίποτα.")
    cursor.close()


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
