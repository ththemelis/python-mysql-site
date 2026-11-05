"""Το πρόγραμμα των δανεισμών (Στάδιο 6). Δεν χρειάζεται να το αλλάξεις.

Μενού με τέσσερις επιλογές. Όλες οι δουλειές με τη βάση γίνονται από το loans.py· εδώ γίνονται μόνο οι ερωτήσεις, τα μηνύματα και ο χειρισμός των
σφαλμάτων. Τρέξε το με: python lending.py
"""

import mysql.connector

import db
import loans
import ui


def show_menu():
    print()
    print("=== ΔΑΝΕΙΣΜΟΙ ===")
    print("1. Εμφάνιση όλων των δανεισμών")
    print("2. Δανεισμός παιχνιδιού")
    print("3. Επιστροφή παιχνιδιού")
    print("4. Έλεγχος συνέπειας")
    print("0. Έξοδος")


def list_loans(connection):
    rows = loans.get_loans(connection)
    print()
    print(f"{'Id':<4}{'Παιχνίδι':<22}{'Μέλος':<10}{'Δανείστηκε':<13}Επιστράφηκε")
    for row in rows:
        returned = "—" if row["returned_on"] is None else row["returned_on"].strftime("%d/%m/%Y")
        print(f"{row['id']:<4}{row['title']:<22}{row['username']:<10}{row['loaned_on'].strftime('%d/%m/%Y'):<13}{returned}")


def lend(connection):
    game_id = ui.ask_int("Id παιχνιδιού: ", 1, 1000000)
    member_id = ui.ask_int("Id μέλους (1-4): ", 1, 1000000)
    try:
        loan_id = loans.lend_game(connection, game_id, member_id)
        print(f"Ο δανεισμός έγινε (id {loan_id}).")
    except mysql.connector.IntegrityError as error:
        if error.errno == 4025:
            print("Δεν υπάρχει διαθέσιμο αντίτυπο αυτού του παιχνιδιού. Δεν έγινε καμία αλλαγή.")
        elif error.errno == 1452:
            print("Δεν υπάρχει παιχνίδι ή μέλος με αυτό το id. Δεν έγινε καμία αλλαγή.")
        else:
            print("Η βάση δεν δέχτηκε τον δανεισμό:", error.msg)


def give_back(connection):
    loan_id = ui.ask_int("Id δανεισμού: ", 1, 1000000)
    if loans.return_game(connection, loan_id):
        print("Η επιστροφή έγινε.")
    else:
        print("Δεν υπάρχει ενεργός δανεισμός με αυτό το id. Δεν έγινε καμία αλλαγή.")


def consistency(connection):
    problems = loans.check_consistency(connection)
    if len(problems) == 0:
        print("Όλα συνεπή: διαθέσιμα + ενεργοί δανεισμοί = 2 για κάθε παιχνίδι.")
    for row in problems:
        print(f"ΑΣΥΝΕΠΕΙΑ: {row['title']}: {row['copies_available']} διαθέσιμα + {row['active_loans']} ενεργοί δανεισμοί, αλλά το παιχνίδι έχει {loans.COPIES} αντίτυπα.")


def main():
    try:
        connection = db.connect()
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        return
    with connection:
        while True:
            connection.commit()          # νέα «φωτογραφία» της βάσης σε κάθε γύρο (Μάθημα 7)
            show_menu()
            choice = input("Επιλογή: ")
            if choice == "1":
                list_loans(connection)
            elif choice == "2":
                lend(connection)
            elif choice == "3":
                give_back(connection)
            elif choice == "4":
                consistency(connection)
            elif choice == "0":
                break
            else:
                print("Γράψε έναν αριθμό από το 0 ως το 4.")


if __name__ == "__main__":
    main()
