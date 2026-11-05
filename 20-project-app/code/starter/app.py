"""Η εφαρμογή του project σου (Μάθημα 20). Τρέξε την με: python app.py

Το μενού και η σύνδεση των modules: ρωτά με το ui, μιλά με τη βάση μέσω του queries, και χειρίζεται τα σφάλματα. Κάθε επιλογή του μενού είναι ΜΙΑ συνάρτηση εδώ, που καλεί ΜΙΑ συνάρτηση
του queries. Η λίστα OPTIONS στο τέλος των συναρτήσεων δένει τα νούμερα του μενού με τις συναρτήσεις: για μια νέα επιλογή γράφεις μια συνάρτηση και προσθέτεις μια γραμμή στη λίστα.

Πρότυπο: το app.py της πιτσαρίας (example/app.py).
"""

import mysql.connector

import db
import queries
import ui

# TODO 1: ο τίτλος του project σου, όπως θα φαίνεται πάνω από το μενού
TITLE = "ΤΙΤΛΟΣ ΤΟΥ PROJECT ΜΟΥ"


# ---------------------------------------------------------------- οι επιλογές του μενού: ΜΙΑ συνάρτηση για κάθε επιλογή
def show_things(connection):
    """Επιλογή 1: εμφανίζει ... (Στάδιο 2: ένα ερώτημα με JOIN)."""
    # TODO 2: κάλεσε τη συνάρτησή σου από το queries και τύπωσε το αποτέλεσμα με ui.print_table(rows, [(κλειδί, τίτλος, πλάτος), ...])
    print("(Η επιλογή αυτή δεν έχει γραφτεί ακόμη.)")


def add_thing(connection):
    """Επιλογή 2: ζητά τα στοιχεία και προσθέτει ... (Στάδιο 3: έλεγχος εισόδου και μηνύματα σφαλμάτων)."""
    # TODO 3: ρώτα με τα ui.ask_text, ui.ask_int, ui.ask_price, ui.ask_digits, ui.ask_choice, κάλεσε το queries και πιάσε το IntegrityError (1062, 1452, ...)
    print("(Η επιλογή αυτή δεν έχει γραφτεί ακόμη.)")


# Τα νούμερα του μενού, τα κείμενά τους και οι συναρτήσεις που τρέχουν (κλειδί, κείμενο, συνάρτηση)
# TODO 4: πρόσθεσε μια γραμμή για κάθε νέα επιλογή (τουλάχιστον 4 επιλογές συνολικά)
OPTIONS = [
    ("1", "Εμφάνιση ...", show_things),
    ("2", "Προσθήκη ...", add_thing),
]


def main():
    try:
        connection = db.connect()
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel, και τα config.py και config_local.py.")
        return

    actions = {}                                # νούμερο μενού -> συνάρτηση
    for key, text, function in OPTIONS:
        actions[key] = function

    with connection:
        while True:
            connection.commit()                 # νέα «φωτογραφία» της βάσης σε κάθε γύρο (Μάθημα 7)
            ui.show_menu(TITLE, OPTIONS)
            choice = input("Επιλογή: ").strip()
            if choice == "0":
                break
            if choice in actions:
                try:
                    actions[choice](connection)
                except mysql.connector.Error as error:
                    print("Σφάλμα της βάσης:", error.msg)
            else:
                print("Γράψε έναν αριθμό από το μενού.")
    print("Γεια σου!")


if __name__ == "__main__":
    main()
