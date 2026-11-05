"""Στάδιο 5: ένα λάθος που ΔΕΝ φαίνεται, το ξεχασμένο rollback. Δεν χρειάζεται να το συμπληρώσεις.

Δανείζουμε το Pixel Racer, που έχει 0 διαθέσιμα αντίτυπα. Το INSERT στον loans πετυχαίνει, το UPDATE στον games αποτυγχάνει (CHECK).
Η έκδοση 1 πιάνει το σφάλμα αλλά ΔΕΝ κάνει rollback· η έκδοση 2 κάνει. Μετά από κάθε έκδοση το πρόγραμμα κάνει ένα απλό commit (όπως το κάνει το μενού κάθε
εφαρμογής μας στην αρχή του βρόχου) και κοιτάζει τη βάση από ΜΙΑ ΑΛΛΗ σύνδεση, που βλέπει μόνο όσα έχουν οριστικοποιηθεί.
"""

import mysql.connector

import db
import lab_data
import loans


def lend_forgetful(connection, game_id, member_id):
    """Δανείζει, αλλά αν η βάση δώσει σφάλμα το πιάνει και συνεχίζει, ΧΩΡΙΣ rollback."""
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO loans (game_id, member_id) VALUES (%s, %s)", (game_id, member_id))
            cursor.execute("UPDATE games SET copies_available = copies_available - 1 WHERE id = %s", (game_id,))
            connection.commit()
        except mysql.connector.Error as error:
            print(f"  η βάση απάντησε: #{error.errno} {error.msg}")
            print("  (το πρόγραμμα πιάνει το σφάλμα και συνεχίζει)")


def lend_careful(connection, game_id, member_id):
    """Το ίδιο, αλλά μετά το σφάλμα κάνει rollback."""
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO loans (game_id, member_id) VALUES (%s, %s)", (game_id, member_id))
            cursor.execute("UPDATE games SET copies_available = copies_available - 1 WHERE id = %s", (game_id,))
            connection.commit()
        except mysql.connector.Error as error:
            connection.rollback()
            print(f"  η βάση απάντησε: #{error.errno} {error.msg}")
            print("  (το πρόγραμμα πιάνει το σφάλμα ΚΑΙ κάνει rollback)")


def report(checker):
    """Τι βλέπει μια άλλη σύνδεση: πόσοι δανεισμοί υπάρχουν και αν τα νούμερα βγάζουν λογαριασμό."""
    checker.rollback()                   # νέα «φωτογραφία» (Μάθημα 7)
    with checker.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM loans")
        count = cursor.fetchone()[0]
    print(f"  Δανεισμοί στη βάση: {count} (πριν ήταν 4)")
    problems = loans.check_consistency(checker)
    if len(problems) == 0:
        print("  Έλεγχος συνέπειας: ΟΚ")
    for row in problems:
        print(
            f"  ΑΣΥΝΕΠΕΙΑ: {row['title']}: {row['copies_available']} διαθέσιμα + {row['active_loans']} ενεργοί δανεισμοί, "
            f"αλλά το παιχνίδι έχει {loans.COPIES} αντίτυπα"
        )


connection = db.connect()
checker = db.connect()
lab_data.reset(connection)

print("=== Έκδοση 1: πιάνει το σφάλμα, ΧΩΡΙΣ rollback ===")
print("Δανεισμός του Pixel Racer (id 2) στο μέλος 4...")
lend_forgetful(connection, 2, 4)
print("Αργότερα το πρόγραμμα κάνει ένα απλό commit (π.χ. στην αρχή του επόμενου γύρου του μενού).")
connection.commit()
print("Η βάση, όπως τη βλέπει ΑΛΛΗ σύνδεση:")
report(checker)

lab_data.reset(connection)

print()
print("=== Έκδοση 2: πιάνει το σφάλμα ΚΑΙ κάνει rollback ===")
print("Δανεισμός του Pixel Racer (id 2) στο μέλος 4...")
lend_careful(connection, 2, 4)
print("Αργότερα το πρόγραμμα κάνει ένα απλό commit.")
connection.commit()
print("Η βάση, όπως τη βλέπει ΑΛΛΗ σύνδεση:")
report(checker)

lab_data.reset(connection)
connection.close()
checker.close()
