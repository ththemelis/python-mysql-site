"""Έλεγχος του project σου (Μάθημα 20). Δεν χρειάζεται να το αλλάξεις.

Τρέξε το μέσα στον φάκελο του project: python check_project.py

Διαβάζει τα αρχεία σου ΩΣ ΚΕΙΜΕΝΟ (δεν συνδέεται με τη βάση και δεν τρέχει το μενού) και ελέγχει τις ελάχιστες απαιτήσεις: τα αρχεία, το μενού, τον έλεγχο εισόδου, την ασφάλεια
(κωδικοί, SQL με παραμέτρους), τη συναλλαγή, το README και τον πίνακα δοκιμών. Για κάθε αποτυχία σου λέει τι να διορθώσεις. Τη βάση σου την ελέγχει το check_project_db.py του Μαθήματος 19.
"""

import os
import re

REQUIRED_FILES = ["app.py", "queries.py", "ui.py", "db.py", "config.py", "01-schema.sql", "README.txt", "test-plan.txt"]
MIN_OPTIONS = 4              # επιλογές στο μενού (χωρίς την έξοδο)
MIN_ASK_CALLS = 3            # κλήσεις ui.ask_… στο app.py (έλεγχος εισόδου)
MIN_TESTS = 10               # δοκιμές στον πίνακα δοκιμών
README_WORDS = ["ΤΙ ΚΑΝΕΙ", "ΠΩΣ ΤΡΕΧΕΙ", "ΜΕΝΟΥ", "ΒΑΣΗ", "ΑΡΧΕΙΑ", "ΔΟΚΙΜΕΣ", "ΟΡΙΑ"]
PLACEHOLDER = "ΣΥΜΠΛΗΡΩΣΕ"

SQL_WORDS = re.compile(r"(SELECT\s|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM)")
PASSWORD_LITERAL = re.compile(r"password\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE)
ROOT_LITERAL = re.compile(r"[\"']root[\"']")
STRING_FORMAT = re.compile(r"[\"']\s*(%\s*[(\w]|\+\s*\w)")        # "…" % (…)  ή  "…" + μεταβλητή


def read(name):
    """Το κείμενο ενός αρχείου, ή None αν δεν υπάρχει."""
    if not os.path.exists(name):
        return None
    with open(name, encoding="utf-8") as stream:
        return stream.read()


def python_files():
    """Τα αρχεία .py του φακέλου που ελέγχονται για ασφάλεια (όχι ο έλεγχος και τα αρχεία κωδικού)."""
    skip = ("check_project.py", "config_local.py", "config_local.example.py")
    return sorted(name for name in os.listdir(".") if name.endswith(".py") and name not in skip)


def code_lines(name):
    """Οι γραμμές ενός αρχείου Python (αριθμός, κείμενο), χωρίς τις γραμμές που είναι μόνο σχόλιο."""
    text = read(name) or ""
    lines = []
    for number, line in enumerate(text.split("\n"), 1):
        if not line.strip().startswith("#"):
            lines.append((number, line))
    return lines


def find_lines(test):
    """Όλες οι γραμμές κώδικα (αρχείο:γραμμή) όπου η συνάρτηση test(γραμμή) δίνει αληθές."""
    found = []
    for name in python_files():
        for number, line in code_lines(name):
            if test(line):
                found.append(f"{name}:{number}")
    return found


def count_options():
    """Πόσες επιλογές έχει η λίστα OPTIONS του app.py. Επιστρέφει (αριθμός ή None, μήνυμα σφάλματος)."""
    try:
        import app
    except Exception as error:                              # ό,τι κι αν πάει στραβά στο import: το δείχνουμε
        return None, f"Το app.py δεν φορτώνει: {type(error).__name__}: {error}"
    options = getattr(app, "OPTIONS", None)
    if not isinstance(options, list):
        return None, "Το app.py δεν έχει λίστα OPTIONS (κλειδί, κείμενο, συνάρτηση)."
    for key, text, function in options:
        if not callable(function):
            return None, f"Η επιλογή «{text}» δεν δείχνει σε συνάρτηση."
    return len(options), ""


def has_transaction(queries_text):
    """Αληθές αν κάποια συνάρτηση του queries.py έχει ΔΥΟ ή περισσότερες εντολές execute ΚΑΙ rollback (δηλαδή συναλλαγή)."""
    for block in queries_text.split("def ")[1:]:
        if "rollback()" in block and block.count("execute") >= 2:
            return True
    return False


def test_rows(text):
    """Οι γραμμές δοκιμών του test-plan.txt: αυτές που αρχίζουν με αριθμό και |."""
    rows = []
    for line in text.split("\n"):
        if re.match(r"^\s*\d+\s*\|", line):
            rows.append(line)
    return rows


def run_checks():
    """Επιστρέφει λίστα ελέγχων: (τίτλος, πέρασε;, λεπτομέρεια, υπόδειξη αν δεν πέρασε)."""
    checks = []
    missing = [name for name in REQUIRED_FILES if read(name) is None]
    checks.append(("Υπάρχουν όλα τα αρχεία του project", len(missing) == 0, "",
                   "Λείπουν: " + ", ".join(missing)))

    broken = []
    for name in python_files():
        try:
            compile(read(name), name, "exec")
        except SyntaxError as error:
            broken.append(f"{name}:{error.lineno}")
    checks.append(("Τα αρχεία .py δεν έχουν συντακτικά λάθη", len(broken) == 0, "", "Σύνταξη (SyntaxError) στο " + ", ".join(broken)))

    options, problem = count_options()
    checks.append((f"Το μενού έχει τουλάχιστον {MIN_OPTIONS} επιλογές", options is not None and options >= MIN_OPTIONS,
                   f"({options})", problem or f"Έχεις {options}. Πρόσθεσε επιλογές στη λίστα OPTIONS του app.py."))

    app_text = read("app.py") or ""
    app_code = "\n".join(line for number, line in code_lines("app.py"))          # χωρίς τις γραμμές-σχόλια
    left = []
    for name in python_files():
        for number, line in enumerate((read(name) or "").splitlines(), 1):
            if "# TODO" in line:
                left.append(f"{name}:{number}")
    for text in ("δεν έχει γραφτεί ακόμη", "ΤΙΤΛΟΣ ΤΟΥ PROJECT ΜΟΥ"):
        if text in app_text:
            left.append(f"app.py «{text}»")
    checks.append(("Δεν έχουν μείνει σχόλια TODO ή κείμενα του σκελετού", len(left) == 0, "", "Δες: " + ", ".join(left[:5])))

    asks = app_code.count("ui.ask_")
    checks.append((f"Το app.py ελέγχει την είσοδο (τουλάχιστον {MIN_ASK_CALLS} κλήσεις ui.ask_…)", asks >= MIN_ASK_CALLS, f"({asks})",
                   "Ρώτα με τα ui.ask_text, ui.ask_int, ui.ask_price, ui.ask_digits, ui.ask_choice: ξαναρωτούν μέχρι να πάρουν σωστή τιμή (Μάθημα 8)."))
    checks.append(("Το app.py πιάνει σφάλματα της βάσης με φιλικό μήνυμα (IntegrityError, errno)", "errno" in app_code, "",
                   "Πιάσε το mysql.connector.IntegrityError και δες το error.errno (1062: υπάρχει ήδη, 1452: δεν υπάρχει ο γονέας), όπως στο παράδειγμα."))

    passwords = find_lines(lambda line: PASSWORD_LITERAL.search(line) is not None)
    checks.append(("Κανένας κωδικός μέσα στον κώδικα (μόνο στο config_local.py)", len(passwords) == 0, "",
                   "Κωδικός γραμμένος στο " + ", ".join(passwords) + ". Βάλ' τον στο config_local.py (Μάθημα 17)."))
    roots = find_lines(lambda line: ROOT_LITERAL.search(line) is not None)
    checks.append(("Η εφαρμογή δεν συνδέεται ως root", len(roots) == 0, "", "Βρέθηκε «root» στο " + ", ".join(roots) + ". Χρησιμοποίησε τον λογαριασμό της εφαρμογής."))

    unsafe = find_lines(lambda line: SQL_WORDS.search(line) is not None and (
        re.search(r"\bf[\"']", line) is not None or ".format(" in line or STRING_FORMAT.search(line) is not None))
    checks.append(("Η SQL δεν φτιάχνεται με f-string, + ή format (μόνο παράμετροι %s)", len(unsafe) == 0, "",
                   "Επικίνδυνη SQL (SQL injection, Μάθημα 17) στο " + ", ".join(unsafe[:5]) + ". Βάλε %s και δώσε τις τιμές ως δεύτερο όρισμα του execute."))

    queries_text = "\n".join(line for number, line in code_lines("queries.py"))     # χωρίς τις γραμμές-σχόλια
    checks.append(("Το queries.py στέλνει τις τιμές με παραμέτρους %s", queries_text.count("%s") >= 3, f"({queries_text.count('%s')})",
                   "Χρησιμοποίησε %s στην SQL και πλειάδα τιμών (Μάθημα 5)."))
    checks.append(("Υπάρχει συναλλαγή: δύο εντολές με ένα commit και rollback", has_transaction(queries_text), "",
                   "Γράψε μια συνάρτηση με δύο ή περισσότερες εντολές execute, ένα commit και rollback + raise στο except (Μάθημα 18)."))

    readme = read("README.txt") or ""
    missing_words = [word for word in README_WORDS if word not in readme]
    checks.append(("Το README.txt είναι συμπληρωμένο (χωρίς «" + PLACEHOLDER + "») και έχει όλα τα τμήματα",
                   readme != "" and PLACEHOLDER not in readme and len(missing_words) == 0, "",
                   ("Σβήσε/συμπλήρωσε τα «" + PLACEHOLDER + "». " if PLACEHOLDER in readme else "") + ("Λείπουν τμήματα: " + ", ".join(missing_words) if missing_words else "")))

    plan = read("test-plan.txt") or ""
    rows = test_rows(plan)
    unresolved = [row for row in rows if row.rstrip().endswith("ΑΠΕΤΥΧΕ")]
    checks.append((f"Ο πίνακας δοκιμών έχει τουλάχιστον {MIN_TESTS} δοκιμές, χωρίς «{PLACEHOLDER}»", len(rows) >= MIN_TESTS and PLACEHOLDER not in plan, f"({len(rows)})",
                   f"Έχεις {len(rows)} δοκιμές" + (" και έχει μείνει το «" + PLACEHOLDER + "»." if PLACEHOLDER in plan else ".")))
    checks.append(("Καμία δοκιμή δεν μένει ΑΠΕΤΥΧΕ χωρίς διόρθωση", len(unresolved) == 0 and len(rows) > 0, "",
                   "Διόρθωσε το πρόγραμμα και ξαναδοκίμασε. Στη γραμμή: «ΑΠΕΤΥΧΕ → διορθώθηκε → ΠΕΤΥΧΕ»."))
    return checks


def main():
    print(f"Έλεγχος του project στον φάκελο «{os.path.basename(os.getcwd())}»")
    print()
    failed = 0
    for title, passed, detail, hint in run_checks():
        if not passed:
            failed += 1
        print(f"{'[OK]    ' if passed else '[ΛΑΘΟΣ]'} {title:<78}{detail if passed else ''}")
        if not passed:
            print(f"         → {hint}")
    print()
    if failed == 0:
        print("Όλοι οι έλεγχοι βγήκαν OK. Τρέξε και το check_project_db.py και δοκίμασε το πρόγραμμα για τελευταία φορά.")
    else:
        print(f"ΛΑΘΟΣ: {failed} απαιτήσεις δεν ικανοποιούνται ακόμη. Διάβασε τα βέλη (→), διόρθωσε και ξανατρέξε.")


if __name__ == "__main__":
    main()
