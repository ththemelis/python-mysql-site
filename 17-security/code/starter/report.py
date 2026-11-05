"""Το πρόγραμμα των αναφορών (Μάθημα 17: με τον λογαριασμό που μόνο διαβάζει).

Το ΔΕΥΤΕΡΟ πρόγραμμα του Μαθήματος 16, που τώρα δεν συνδέεται ως ο λογαριασμός της εφαρμογής αλλά ως ο game_reader: αφού μόνο διαβάζει, δεν
χρειάζεται δικαίωμα να αλλάξει δεδομένα. Τρέξε το: python report.py

Συμπλήρωσε τα δύο κενά (____).
"""

import mysql.connector

import config
import db
import reports
import export
import ui

# Οι στήλες κάθε αναφοράς: ζεύγη (κλειδί του λεξικού, τίτλος της στήλης)
GENRE_COLUMNS = [("genre", "Είδος"), ("games_n", "Παιχνίδια"), ("average", "Μέση τιμή")]
RATING_COLUMNS = [("title", "Τίτλος"), ("reviews_n", "Κριτικές"), ("average_stars", "Μέσος όρος αστεριών")]
PLATFORM_COLUMNS = [("platform", "Πλατφόρμα"), ("games_n", "Παιχνίδια"), ("average", "Μέση τιμή")]


def print_table(columns, rows):
    """Εμφανίζει μια αναφορά ως πίνακα στην οθόνη (το κενό κελί είναι None στη βάση)."""
    print()
    header = ""
    for key, title in columns:
        header = header + f"{title:<22}"
    print(header)
    print("-" * len(header))

    for row in rows:
        line = ""
        for key, title in columns:
            line = line + f"{export.format_value(row[key]):<22}"
        print(line)
    print(f"Γραμμές: {len(rows)}")


def show_report(title, columns, rows, filename):
    """Εμφανίζει μια αναφορά στην οθόνη και ρωτά αν θα αποθηκευτεί σε αρχείο CSV."""
    print()
    print(title)
    print_table(columns, rows)

    answer = input(f"Να αποθηκευτεί στο αρχείο {filename}; (ναι/όχι): ")
    if answer == "ναι":
        count = export.write_csv(filename, columns, rows)
        print(f"Αποθηκεύτηκε το {filename} ({count} γραμμές).")


def run_reports(connection):
    """Το μενού των αναφορών: τρέχει ώσπου ο χρήστης να διαλέξει έξοδο."""
    while True:
        print()
        print("=== ΑΝΑΦΟΡΕΣ ===")
        print("1. Παιχνίδια ανά είδος")
        print("2. Βαθμολογίες παιχνιδιών")
        print("3. Παιχνίδια ανά πλατφόρμα")
        print("0. Έξοδος")
        choice = input("Επιλογή: ")

        if choice == "1":
            rows = reports.games_per_genre(connection)
            show_report("ΠΑΙΧΝΙΔΙΑ ΑΝΑ ΕΙΔΟΣ", GENRE_COLUMNS, rows, "report-genres.csv")
        elif choice == "2":
            min_reviews = ui.ask_int("Τουλάχιστον πόσες κριτικές να έχει το παιχνίδι; (1 έως 10): ", 1, 10)
            rows = reports.ratings_per_game(connection, min_reviews)
            show_report("ΒΑΘΜΟΛΟΓΙΕΣ ΠΑΙΧΝΙΔΙΩΝ", RATING_COLUMNS, rows, "report-ratings.csv")
        elif choice == "3":
            rows = reports.games_per_platform(connection)
            show_report("ΠΑΙΧΝΙΔΙΑ ΑΝΑ ΠΛΑΤΦΟΡΜΑ", PLATFORM_COLUMNS, rows, "report-platforms.csv")
        elif choice == "0":
            break
        else:
            print("Άγνωστη επιλογή. Γράψε έναν από τους αριθμούς του μενού.")


def main():
    """Το κύριο πρόγραμμα: ανοίγει τη σύνδεση και τρέχει το μενού των αναφορών."""
    try:
        # TODO 1: ο λογαριασμός των αναφορών (μόνο διαβάζει), από το config
        user = config.____
        # TODO 2: ο κωδικός του, από το config
        password = config.____
        with db.connect(user, password) as connection:
            run_reports(connection)
    except mysql.connector.Error as error:
        print("Σφάλμα της βάσης:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel.")


if __name__ == "__main__":
    main()
