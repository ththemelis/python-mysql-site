"""Στάδιο 3 — Η εφαρμογή με μενού, με έλεγχο της εισόδου.

Η εφαρμογή του Μαθήματος 7, με τις συναρτήσεις ask_text, ask_int και ask_price να φροντίζουν ό,τι πληκτρολογεί ο
χρήστης. Η add_game και η change_price δεν καλούν πια τις int() και Decimal() απευθείας: δεν μπορούν να
σταματήσουν με ValueError.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal, InvalidOperation

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


def ask_text(message):
    """Ρωτά ώσπου ο χρήστης να γράψει κάτι (όχι κενό) και επιστρέφει το κείμενο, χωρίς κενά στις άκρες."""
    while True:
        text = input(message).strip()
        if text != "":
            return text
        print("Το πεδίο δεν μπορεί να μένει κενό.")


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


def ask_price(message):
    """Ρωτά ώσπου ο χρήστης να γράψει τιμή από 0.01 έως 999.99 (δέχεται και κόμμα) και την επιστρέφει ως Decimal."""
    while True:
        text = input(message).replace(",", ".")
        try:
            price = Decimal(text)
            if Decimal("0.01") <= price <= Decimal("999.99"):
                return price
            print("Η τιμή πρέπει να είναι από 0.01 έως 999.99.")
        except InvalidOperation:
            print("Γράψε έναν αριθμό, π.χ. 3.49.")


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
    """Ζητά τα στοιχεία ενός παιχνιδιού (με έλεγχο) και το προσθέτει στη βάση."""
    # TODO 1: ask_text για κείμενο, ask_int για ακέραιο, ask_price για τιμή (όπως στο Στάδιο 2)
    title = ____("Τίτλος: ")
    genre = ask_text("Είδος: ")
    year = ____("Χρονιά (1970 έως 2100): ", 1970, 2100)
    price = ____("Τιμή (0.01 έως 999.99): ")

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO games (title, genre, release_year, price) VALUES (%s, %s, %s, %s)",
        (title, genre, year, price),
    )
    connection.commit()
    print(f"Προστέθηκε το «{title}» με id {cursor.lastrowid}.")
    cursor.close()


def change_price(connection):
    """Ζητά το id ενός παιχνιδιού και τη νέα τιμή του (με έλεγχο), και αλλάζει την τιμή."""
    # TODO 2: το id είναι ακέραιος από 1 έως 100000
    game_id = ____("id παιχνιδιού: ", 1, 100000)
    price = ask_price("Νέα τιμή (0.01 έως 999.99): ")

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
        return None
    return row[0]


def delete_game(connection):
    """Ζητά ένα id, δείχνει τον τίτλο, ζητά επιβεβαίωση και σβήνει το παιχνίδι."""
    game_id = ask_int("id παιχνιδιού που θα σβηστεί: ", 1, 100000)

    title = find_title(connection, game_id)
    if title is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    answer = input(f"Να σβηστεί το «{title}»; (ναι/όχι): ")
    if answer != "ναι":
        print("Ακυρώθηκε. Δεν σβήστηκε τίποτα.")
        return

    cursor = connection.cursor()
    cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
    if cursor.rowcount == 1:
        connection.commit()
        print("Το παιχνίδι σβήστηκε.")
    else:
        connection.rollback()
        print("Κάτι πήγε στραβά. Δεν άλλαξε τίποτα.")
    cursor.close()


def main():
    """Το κύριο πρόγραμμα: ανοίγει τη σύνδεση και τρέχει το μενού ώσπου ο χρήστης να διαλέξει έξοδο."""
    connection = connect()

    while True:
        # Τελειώνει κάθε ανοιχτή συναλλαγή, ώστε η εφαρμογή να βλέπει τα τελευταία δεδομένα της βάσης
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
