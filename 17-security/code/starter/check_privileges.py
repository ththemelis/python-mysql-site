"""Έλεγχος του Σταδίου 2: δοκιμάζει τι μπορεί και τι ΔΕΝ μπορεί να κάνει κάθε λογαριασμός. Δεν χρειάζεται να το συμπληρώσεις.

Συνδέεται ως game_app και ως game_reader (με τα config και db που συμπλήρωσες) και δοκιμάζει εντολές. Δεν αλλάζει δεδομένα: τα UPDATE και DELETE
δεν ταιριάζουν σε καμία γραμμή (id 0) και ό,τι τρέξει ακυρώνεται με rollback.
"""

import mysql.connector

import config
import db

CREATE_TEST = "CREATE TABLE zz_privilege_test (id INT)"

# Κάθε δοκιμή: (τίτλος, εντολή SQL, επιτρέπεται;)
APP_TESTS = [
    ("SELECT από τον games", "SELECT COUNT(*) FROM games", True),
    ("UPDATE στον games", "UPDATE games SET price = price WHERE id = 0", True),
    ("DELETE από τον games", "DELETE FROM games WHERE id = 0", True),
    ("CREATE TABLE (νέος πίνακας)", CREATE_TEST, False),
    ("SELECT από τον mysql.user", "SELECT COUNT(*) FROM mysql.user", False),
]
READER_TESTS = [
    ("SELECT από τον games", "SELECT COUNT(*) FROM games", True),
    ("UPDATE στον games", "UPDATE games SET price = price WHERE id = 0", False),
    ("DELETE από τον games", "DELETE FROM games WHERE id = 0", False),
    ("CREATE TABLE (νέος πίνακας)", CREATE_TEST, False),
    ("SELECT από τον mysql.user", "SELECT COUNT(*) FROM mysql.user", False),
]


def try_sql(connection, sql):
    """Τρέχει μια εντολή. Επιστρέφει (True, None) αν επιτράπηκε, αλλιώς (False, το σφάλμα της βάσης)."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor.with_rows:
                cursor.fetchall()
        connection.rollback()
        return True, None
    except mysql.connector.Error as error:
        return False, error


def check_account(user, password, tests):
    """Δοκιμάζει έναν λογαριασμό. Επιστρέφει πόσοι έλεγχοι ΔΕΝ βγήκαν όπως αναμενόταν."""
    print()
    print(f"=== Λογαριασμός {user} ===")
    try:
        connection = db.connect(user, password)
    except mysql.connector.Error as error:
        print(f"Δεν μπόρεσα να συνδεθώ: #{error.errno} {error.msg}")
        print("Έλεγξε ότι έτρεξες το 02-users.sql και ότι το config_local.py έχει τον σωστό κωδικό.")
        return len(tests) + 1

    wrong = 0
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT CURRENT_USER()")
            who = cursor.fetchone()[0]
        verdict = "OK" if who == f"{user}@localhost" else "ΛΑΘΟΣ"
        if verdict == "ΛΑΘΟΣ":
            wrong += 1
        print(f"{'Ποιος είμαι (CURRENT_USER)':<32}{who:<26}{verdict}")

        first_denial = None
        for title, sql, should_work in tests:
            worked, error = try_sql(connection, sql)
            if worked:
                result = "επιτρέπεται"
            else:
                result = f"ΑΠΑΓΟΡΕΥΤΗΚΕ (#{error.errno})"
                if first_denial is None:
                    first_denial = error.msg
            verdict = "OK" if worked == should_work else "ΛΑΘΟΣ"
            if verdict == "ΛΑΘΟΣ":
                wrong += 1
            print(f"{title:<32}{result:<26}{verdict}")
            if sql == CREATE_TEST and worked:
                try_sql(connection, "DROP TABLE zz_privilege_test")
                print("  (Ο λογαριασμός μπόρεσε να φτιάξει πίνακα! Τον έσβησα, αλλά έλεγξε τα GRANT.)")

    if first_denial is not None:
        print("Μήνυμα της βάσης για την πρώτη απαγόρευση:")
        print("  " + first_denial)
    return wrong


problems = check_account(config.APP_USER, config.APP_PASSWORD, APP_TESTS)
problems += check_account(config.READER_USER, config.READER_PASSWORD, READER_TESTS)

print()
if problems == 0:
    print("Όλοι οι έλεγχοι βγήκαν όπως αναμενόταν.")
else:
    print(f"ΛΑΘΟΣ: {problems} έλεγχοι δεν βγήκαν όπως αναμενόταν. Δες τα GRANT του 02-users.sql και το db.py.")
