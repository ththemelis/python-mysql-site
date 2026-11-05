"""Η εφαρμογή «Βιβλιοθήκη παιχνιδιών».

Το μενού και η σύνδεση των modules: ρωτά με το ui, μιλά με τη βάση μέσω του queries, και χειρίζεται τα σφάλματα.
Τρέχεις μόνο αυτό το αρχείο: python app.py
"""

from datetime import date

import mysql.connector

import db
import queries
import ui

# Η παλαιότερη ημερομηνία προσθήκης που δέχεται η εφαρμογή (το ίδιο όριο έχει και ο περιορισμός CHECK της βάσης)
EARLIEST = date(2020, 1, 1)


def list_games(connection):
    """Επιλογή 1: εμφανίζει όλα τα παιχνίδια."""
    ui.print_games(queries.get_games(connection))


def search_games(connection):
    """Επιλογή 2: ζητά μέρος του τίτλου και εμφανίζει τα παιχνίδια που τον περιέχουν."""
    text = input("Μέρος του τίτλου: ")
    rows = queries.search_games(connection, text)

    if len(rows) == 0:
        print("Δεν βρέθηκε κανένα παιχνίδι.")
    else:
        ui.print_games(rows)


def add_game(connection):
    """Επιλογή 3: ζητά τα στοιχεία ενός παιχνιδιού και των πλατφορμών του και τα προσθέτει."""
    title = ui.ask_text("Τίτλος: ")
    genre_id = ui.ask_genre(queries.get_genres(connection))
    year = ui.ask_int("Χρονιά (1970 έως 2100): ", 1970, 2100)
    price = ui.ask_price("Τιμή (0.01 έως 999.99): ")
    description = input("Περιγραφή (Enter για καμία): ").strip()
    if description == "":
        description = None          # το None της Python γίνεται NULL στη βάση
    added_on = ui.ask_date(
        "Ημερομηνία προσθήκης (ΗΗ/ΜΜ/ΕΕΕΕ, Enter για σήμερα): ", EARLIEST, date.today(), default=date.today()
    )
    platform_ids = ui.ask_platforms(queries.get_platforms(connection))

    try:
        game_id = queries.add_game(connection, title, genre_id, year, price, description, added_on, platform_ids)
        print(f"Προστέθηκε το «{title}» με id {game_id} και {len(platform_ids)} πλατφόρμες.")
    except mysql.connector.IntegrityError as error:
        if error.errno == 1062:
            print(f"Υπάρχει ήδη παιχνίδι με τίτλο «{title}».")
        elif error.errno == 1452:
            print("Το είδος ή η πλατφόρμα που διάλεξες δεν υπάρχει.")
        else:
            print("Η βάση δεν δέχτηκε τα δεδομένα:", error.msg)


def change_price(connection):
    """Επιλογή 4: ζητά το id ενός παιχνιδιού και τη νέα τιμή του, και αλλάζει την τιμή."""
    game_id = ui.ask_int("id παιχνιδιού: ", 1, 100000)
    price = ui.ask_price("Νέα τιμή (0.01 έως 999.99): ")

    changed = queries.change_price(connection, game_id, price)
    if changed == 0:
        print("Δεν άλλαξε καμία γραμμή: ή δεν υπάρχει τέτοιο id ή η τιμή ήταν ήδη αυτή.")
    else:
        print(f"Η τιμή του παιχνιδιού με id {game_id} έγινε {price} €.")


def delete_game(connection):
    """Επιλογή 5: ζητά ένα id, δείχνει τον τίτλο, ζητά επιβεβαίωση και σβήνει το παιχνίδι."""
    game_id = ui.ask_int("id παιχνιδιού που θα σβηστεί: ", 1, 100000)

    title = queries.find_title(connection, game_id)
    if title is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    answer = input(f"Να σβηστεί το «{title}»; (ναι/όχι): ")
    if answer != "ναι":
        print("Ακυρώθηκε. Δεν σβήστηκε τίποτα.")
        return

    try:
        if queries.delete_game(connection, game_id):
            print("Το παιχνίδι σβήστηκε.")
        else:
            print("Κάτι πήγε στραβά. Δεν άλλαξε τίποτα.")
    except mysql.connector.IntegrityError as error:
        if error.errno == 1451:
            print("Το παιχνίδι έχει κριτικές και δεν μπορεί να σβηστεί. Σβήσε πρώτα τις κριτικές του.")
        else:
            print("Η βάση δεν δέχτηκε την αλλαγή:", error.msg)


def games_since(connection):
    """Επιλογή 6: ζητά μια ημερομηνία και εμφανίζει τα παιχνίδια που προστέθηκαν από τότε και μετά."""
    since = ui.ask_date("Από ημερομηνία (ΗΗ/ΜΜ/ΕΕΕΕ): ", EARLIEST, date.today())
    rows = queries.games_since(connection, since)

    if len(rows) == 0:
        print("Κανένα παιχνίδι δεν προστέθηκε από εκείνη την ημερομηνία.")
    else:
        ui.print_games(rows)


def reviews_of_game(connection):
    """Επιλογή 7: ζητά ένα id και εμφανίζει τις κριτικές του παιχνιδιού."""
    game_id = ui.ask_int("id παιχνιδιού: ", 1, 100000)
    ui.print_reviews(queries.get_reviews(connection, game_id))


def platforms_of_game(connection):
    """Επιλογή 8: ζητά ένα id και εμφανίζει τις πλατφόρμες του παιχνιδιού."""
    game_id = ui.ask_int("id παιχνιδιού: ", 1, 100000)
    ui.print_platforms(queries.get_platforms_of_game(connection, game_id))


def run_menu(connection):
    """Το μενού: τρέχει ώσπου ο χρήστης να διαλέξει έξοδο."""
    while True:
        try:
            if not connection.is_connected():
                print("Χάθηκε η σύνδεση με τη βάση. Η εφαρμογή τερματίζεται.")
                break
            # Τελειώνει κάθε ανοιχτή συναλλαγή, ώστε η εφαρμογή να βλέπει τα τελευταία δεδομένα της βάσης
            connection.commit()
            ui.show_menu()
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
            elif choice == "6":
                games_since(connection)
            elif choice == "7":
                reviews_of_game(connection)
            elif choice == "8":
                platforms_of_game(connection)
            elif choice == "0":
                break
            else:
                print("Άγνωστη επιλογή. Γράψε έναν από τους αριθμούς του μενού.")
        except mysql.connector.Error as error:
            print("Σφάλμα της βάσης:", error.msg)


def main():
    """Το κύριο πρόγραμμα: ανοίγει τη σύνδεση, τρέχει το μενού και κλείνει τη σύνδεση."""
    try:
        with db.connect() as connection:
            run_menu(connection)
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel.")
        return

    print("Γεια σου!")


if __name__ == "__main__":
    main()
