"""Στάδιο 5 — Η εφαρμογή πιάνει και τα σφάλματα της βάσης.

Δουλεύει ΜΕΤΑ το Στάδιο 4 (ο games έχει πια UNIQUE στον τίτλο και τη στήλη description). Η add_game ρωτά και μια
προαιρετική περιγραφή (κενό = NULL) και πιάνει το σφάλμα όταν ο τίτλος υπάρχει ήδη. Η main πιάνει τα υπόλοιπα
σφάλματα της βάσης και το σφάλμα σύνδεσης.

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
    title = ask_text("Τίτλος: ")
    genre = ask_text("Είδος: ")
    year = ask_int("Χρονιά (1970 έως 2100): ", 1970, 2100)
    price = ask_price("Τιμή (0.01 έως 999.99): ")
    description = input("Περιγραφή (Enter για καμία): ").strip()
    if description == "":
        description = None          # το None της Python γίνεται NULL στη βάση

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO games (title, genre, release_year, price, description) VALUES (%s, %s, %s, %s, %s)",
            (title, genre, year, price, description),
        )
        connection.commit()
        print(f"Προστέθηκε το «{title}» με id {cursor.lastrowid}.")
    # TODO 1: οι περιορισμοί της βάσης (UNIQUE, NOT NULL, CHECK) δίνουν σφάλμα τύπου IntegrityError
    except mysql.connector.____ as error:
        # TODO 2: ακύρωσε ό,τι δεν ολοκληρώθηκε
        connection.____()
        # TODO 3: ο αριθμός του σφάλματος είναι η ιδιότητα errno· το 1062 σημαίνει «διπλή τιμή» σε στήλη UNIQUE
        if error.____ == 1062:
            print(f"Υπάρχει ήδη παιχνίδι με τίτλο «{title}».")
        else:
            print("Η βάση δεν δέχτηκε τα δεδομένα:", error.msg)
    cursor.close()


def change_price(connection):
    """Ζητά το id ενός παιχνιδιού και τη νέα τιμή του (με έλεγχο), και αλλάζει την τιμή."""
    game_id = ask_int("id παιχνιδιού: ", 1, 100000)
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
    # TODO 4: αν η MySQL δεν τρέχει, η connect() δίνει σφάλμα του οδηγού· η Error τα πιάνει όλα (είναι η «μητέρα» τους)
    try:
        connection = connect()
    except mysql.connector.____ as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel.")
        return

    while True:
        # Η κάθε ενέργεια μπορεί να αποτύχει με σφάλμα της βάσης: το πιάνουμε εδώ, ώστε η εφαρμογή να μη σταματά
        try:
            # Αν η σύνδεση χάθηκε (π.χ. σταμάτησε η MySQL), δεν έχει νόημα να συνεχίσουμε
            if not connection.is_connected():
                print("Χάθηκε η σύνδεση με τη βάση. Η εφαρμογή τερματίζεται.")
                break
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
        except mysql.connector.Error as error:
            print("Σφάλμα της βάσης:", error.msg)

    connection.close()
    print("Γεια σου!")


main()
