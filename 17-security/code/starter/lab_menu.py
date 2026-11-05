"""Το μενού του εργαστηρίου SQL injection. Δεν χρειάζεται να το αλλάξεις.

Το χρησιμοποιούν τα lab_unsafe.py και lab_safe.py. Ρωτά με ποιον λογαριασμό θα τρέξει το εργαστήριο και μετά, σε κάθε επανάληψη, ζητά στοιχεία
σύνδεσης μέλους ή κείμενο αναζήτησης και τα δίνει στις δύο συναρτήσεις που παίρνει ως ορίσματα. Κρατά ΜΙΑ σύνδεση ανοιχτή (η σύνδεση με τη βάση αργεί
λίγο). Μια επίθεση με δύο εντολές όμως μπορεί να την αφήσει σε άκυρη κατάσταση: πριν από κάθε ενέργεια την ελέγχουμε και, αν χάλασε, ανοίγουμε νέα.
"""

import mysql.connector

import db


def choose_account():
    """Ρωτά ποιος λογαριασμός θα τρέξει το εργαστήριο. Επιστρέφει "1" (game_app) ή "2" (root)."""
    print("Με ποιον λογαριασμό να τρέξει το εργαστήριο;")
    print("1. game_app (ο λογαριασμός της εφαρμογής)")
    print("2. root (ο διαχειριστής: ΜΟΝΟ για να δεις τη διαφορά)")
    while True:
        choice = input("Επιλογή: ")
        if choice in ("1", "2"):
            return choice
        print("Γράψε 1 ή 2.")


def open_connection(account):
    """Ανοίγει νέα σύνδεση με τον λογαριασμό που διαλέχτηκε."""
    if account == "2":
        return db.connect("root", "")
    return db.connect()


def still_works(connection):
    """Αληθές αν η σύνδεση δουλεύει ακόμη. Το rollback τελειώνει και την ανοιχτή συναλλαγή, ώστε να βλέπουμε τα τελευταία δεδομένα."""
    try:
        connection.rollback()
        return True
    except Exception:
        return False


def login(login_function, connection):
    """Ζητά όνομα και κωδικό και τα δίνει στη συνάρτηση σύνδεσης."""
    username = input("Όνομα χρήστη: ")
    password = input("Κωδικός: ")
    member = login_function(connection, username, password)
    if member is None:
        print("Λάθος στοιχεία.")
    else:
        print(f"Συνδέθηκες! id {member[0]}, ρόλος {member[1]}.")


def search(search_function, connection):
    """Ζητά κείμενο και το δίνει στη συνάρτηση αναζήτησης."""
    text = input("Μέρος του τίτλου: ")
    rows = search_function(connection, text)
    if len(rows) == 0:
        print("Δεν βρέθηκε τίποτα.")
    for title, price in rows:
        print(f"{title:<20}{price}")


def run(title, login_function, search_function):
    """Το μενού του εργαστηρίου."""
    print(title)
    account = choose_account()
    name = "game_app" if account == "1" else "root"
    try:
        connection = open_connection(account)
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ:", error.msg)
        return

    while True:
        print()
        print(f"=== {title} (λογαριασμός: {name}) ===")
        print("1. Σύνδεση μέλους")
        print("2. Αναζήτηση παιχνιδιού")
        print("0. Έξοδος")
        choice = input("Επιλογή: ")
        if choice == "0":
            break

        try:
            if not still_works(connection):
                connection.close()
                connection = open_connection(account)
            if choice == "1":
                login(login_function, connection)
            elif choice == "2":
                search(search_function, connection)
            else:
                print("Άγνωστη επιλογή.")
        except mysql.connector.Error as error:
            print("Σφάλμα της βάσης:", error.msg)

    connection.close()
