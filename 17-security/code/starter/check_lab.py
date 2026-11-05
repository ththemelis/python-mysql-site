"""Έλεγχος του Σταδίου 5: τρέχει τις ΙΔΙΕΣ επιθέσεις στην ευπαθή και στην ασφαλή έκδοση, με τον λογαριασμό game_app. Δεν χρειάζεται να το συμπληρώσεις.

Τρέξε πρώτα το 03-members.sql. Καμία από τις δοκιμές δεν σβήνει ή αλλάζει δεδομένα.
"""

import contextlib
import io

import mysql.connector

import db
import lab_safe
import lab_unsafe

MEMBER_NAMES = ("maria", "nikos", "eleni", "admin")

# Κάθε περίπτωση: (είδος, περιγραφή, πρώτη τιμή, δεύτερη τιμή, είναι επίθεση;)
CASES = [
    ("login", "Σύνδεση maria, σωστός κωδικός", "maria", "maria-2026", False),
    ("login", "Σύνδεση maria, λάθος κωδικός", "maria", "wrong", False),
    ("search", "Αναζήτηση «Pixel»", "Pixel", None, False),
    ("login", "ΕΠΙΘΕΣΗ 1: όνομα admin'#", "admin'#", "x", True),
    ("login", "ΕΠΙΘΕΣΗ 2: όνομα ' OR '1'='1'#", "' OR '1'='1'#", "x", True),
    ("search", "ΕΠΙΘΕΣΗ 3: UNION με τον members", "zzz%' UNION SELECT username, password_hash FROM members #", None, True),
]

# Τι πρέπει να δώσει η ΑΣΦΑΛΗΣ έκδοση σε κάθε περίπτωση
EXPECTED_SAFE = ["συνδέθηκε ως member", "απορρίφθηκε", "2 παιχνίδια", "απορρίφθηκε", "απορρίφθηκε", "0 παιχνίδια"]


def describe_login(member, attack):
    if member is None:
        return "απορρίφθηκε"
    if attack:
        return f"ΜΠΗΚΕ ως {member[1]}"
    return f"συνδέθηκε ως {member[1]}"


def describe_search(rows):
    leaked = [row for row in rows if row[0] in MEMBER_NAMES]
    if len(leaked) > 0:
        return f"ΔΙΕΡΡΕΥΣΑΝ {len(leaked)} μέλη"
    return f"{len(rows)} παιχνίδια"


def run_all(login_function, search_function):
    """Τρέχει όλες τις περιπτώσεις με μία σύνδεση και επιστρέφει τα αποτελέσματα ως λίστα από κείμενα."""
    results = []
    with db.connect() as connection:
        for kind, title, first, second, attack in CASES:
            try:
                with contextlib.redirect_stdout(io.StringIO()):          # κρύβει το «SQL που στάλθηκε»
                    if kind == "login":
                        result = login_function(connection, first, second)
                    else:
                        result = search_function(connection, first)
                connection.rollback()
            except mysql.connector.Error as error:
                results.append(f"σφάλμα #{error.errno}")
                continue
            if kind == "login":
                results.append(describe_login(result, attack))
            else:
                results.append(describe_search(result))
    return results


unsafe_results = run_all(lab_unsafe.login_unsafe, lab_unsafe.search_unsafe)
safe_results = run_all(lab_safe.login_safe, lab_safe.search_safe)

print(f"{'Περίπτωση':<38}{'Ευπαθής έκδοση':<24}{'Ασφαλής έκδοση'}")
print("-" * 78)
wrong = 0
for case, unsafe_result, safe_result, expected in zip(CASES, unsafe_results, safe_results, EXPECTED_SAFE):
    print(f"{case[1]:<38}{unsafe_result:<24}{safe_result}")
    if safe_result != expected:
        wrong += 1

print()
if wrong == 0:
    print("Η ασφαλής έκδοση άντεξε και στις τρεις επιθέσεις και δουλεύει κανονικά με σωστά στοιχεία.")
else:
    print(f"ΛΑΘΟΣ: η ασφαλής έκδοση δεν έδωσε το αναμενόμενο σε {wrong} περιπτώσεις. Δες το lab_safe.py.")
