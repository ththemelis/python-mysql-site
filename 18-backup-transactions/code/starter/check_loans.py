"""Έλεγχος του Σταδίου 6. Δεν χρειάζεται να το συμπληρώσεις.

Δοκιμάζει τις συναρτήσεις του loans.py. Χρησιμοποιεί ΔΥΟ συνδέσεις: η μία κάνει τις δανειστικές κινήσεις, η άλλη βλέπει μόνο όσα έχουν
οριστικοποιηθεί. Πριν και μετά ξαναφέρνει τα δεδομένα στην κατάσταση του 02-loans.sql (lab_data.reset), άρα μπορείς να το τρέξεις όσες φορές θέλεις.
"""

import mysql.connector

import db
import lab_data
import loans


def count_loans(connection, refresh=True):
    """Πόσοι δανεισμοί. Με refresh=True ξεκινά νέα «φωτογραφία» (rollback) και βλέπει ό,τι έχει οριστικοποιηθεί. Με refresh=False ΔΕΝ αγγίζει τη συναλλαγή."""
    if refresh:
        connection.rollback()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM loans")
        return cursor.fetchone()[0]


def copies_of(connection, game_id):
    connection.rollback()
    with connection.cursor() as cursor:
        cursor.execute("SELECT copies_available FROM games WHERE id = %s", (game_id,))
        return cursor.fetchone()[0]


def consistent(connection):
    connection.rollback()
    return len(loans.check_consistency(connection)) == 0


wrong = 0


def check(title, ok, hint=""):
    """Τυπώνει το αποτέλεσμα ενός ελέγχου. Η υπόδειξη (hint) φαίνεται μόνο όταν ο έλεγχος αποτύχει."""
    global wrong
    if not ok:
        wrong += 1
    print(f"{title:<66}{'OK' if ok else 'ΛΑΘΟΣ' + ('  ' + hint if hint else '')}")


worker = db.connect()
viewer = db.connect()
lab_data.reset(worker)

print("--- Αρχική κατάσταση")
check("4 δανεισμοί, οι αριθμοί βγάζουν λογαριασμό", count_loans(viewer) == 4 and consistent(viewer))

print("--- Δανεισμός με διαθέσιμο αντίτυπο (Star Dodger, 1 διαθέσιμο)")
new_id = loans.lend_game(worker, 1, 4)
check("lend_game(1, 4) επέστρεψε id δανεισμού", isinstance(new_id, int))
check("η άλλη σύνδεση βλέπει 5 δανεισμούς και 0 αντίτυπα", count_loans(viewer) == 5 and copies_of(viewer, 1) == 0)
check("συνέπεια", consistent(viewer))

print("--- Δανεισμός χωρίς διαθέσιμο αντίτυπο (Pixel Racer, 0 διαθέσιμα)")
try:
    loans.lend_game(worker, 2, 4)
    check("η lend_game(2, 4) ξαναπέταξε το σφάλμα 4025", False, "δεν έγινε κανένα σφάλμα: λείπει το raise;")
except mysql.connector.IntegrityError as error:
    check("η lend_game(2, 4) ξαναπέταξε το σφάλμα 4025", error.errno == 4025, f"βγήκε #{error.errno}")
check("στην ΙΔΙΑ σύνδεση ο δανεισμός δεν έμεινε μισός (5 δανεισμοί)", count_loans(worker, refresh=False) == 5, "έμεινε μισός δανεισμός: λείπει το rollback;")
worker.commit()                          # ένα απλό commit, όπως στο μενού
check("μετά από ένα commit η άλλη σύνδεση βλέπει 5 δανεισμούς", count_loans(viewer) == 5)
check("συνέπεια", consistent(viewer))

print("--- Επιστροφή")
check("return_game(νέος δανεισμός) επέστρεψε True", loans.return_game(worker, new_id) is True)
check("το Star Dodger έχει πάλι 1 διαθέσιμο αντίτυπο", copies_of(viewer, 1) == 1)
check("δεύτερη επιστροφή του ίδιου δανεισμού: False", loans.return_game(worker, new_id) is False)
check("επιστροφή δανεισμού που δεν υπάρχει (id 999): False", loans.return_game(worker, 999) is False)
check("συνέπεια", consistent(viewer))

print("--- Γράψε εσύ: lend_many")
if hasattr(loans, "lend_many"):
    ids = loans.lend_many(worker, [3, 1], 4)
    check("lend_many([3, 1], 4): δύο δανεισμοί", len(ids) == 2)
    check("τα παιχνίδια 3 και 1 έχουν 1 και 0 διαθέσιμα", copies_of(viewer, 3) == 1 and copies_of(viewer, 1) == 0)
    before = count_loans(viewer)
    try:
        loans.lend_many(worker, [4, 2], 4)
        check("η lend_many([4, 2], 4) απέτυχε (το 2 δεν έχει αντίτυπο)", False, "δεν έγινε κανένα σφάλμα")
    except mysql.connector.IntegrityError:
        check("η lend_many([4, 2], 4) απέτυχε (το 2 δεν έχει αντίτυπο)", True)
    worker.commit()
    check("κανένα από τα δύο δεν δανείστηκε: το παιχνίδι 4 έχει ακόμη 2", copies_of(viewer, 4) == 2 and count_loans(viewer) == before)
    check("συνέπεια", consistent(viewer))
else:
    print("(Δεν έχεις γράψει ακόμη τη lend_many στο loans.py: το παραλείπω.)")

lab_data.reset(worker)
worker.close()
viewer.close()

print()
if wrong == 0:
    print("Όλοι οι έλεγχοι βγήκαν όπως αναμενόταν.")
else:
    print(f"ΛΑΘΟΣ: {wrong} έλεγχοι δεν βγήκαν όπως αναμενόταν. Δες το loans.py.")
