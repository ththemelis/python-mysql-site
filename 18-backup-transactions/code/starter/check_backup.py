"""Έλεγχος αντιγράφου ασφαλείας (Στάδιο 3). Δεν χρειάζεται να το συμπληρώσεις.

Δείχνει τα αρχεία .sql του φακέλου backups, ρωτά ποιο να ελέγξει και το διαβάζει γραμμή γραμμή (όπως στο Μάθημα 16). Μετρά τι περιέχει:
πίνακες και γραμμές, εντολές DROP TABLE, περιορισμούς CHECK και λογαριασμούς. Δεν συνδέεται με τη βάση: κοιτάζει μόνο το ίδιο το αρχείο.
"""

import os

import config
import ui


def list_backups(folder):
    """Τα ονόματα των αρχείων .sql του φακέλου, σε αλφαβητική σειρά. Αν ο φάκελος δεν υπάρχει, επιστρέφει κενή λίστα."""
    if not os.path.isdir(folder):
        return []
    names = []
    for name in os.listdir(folder):
        if name.endswith(".sql"):
            names.append(name)
    return sorted(names)


def inspect(path):
    """Διαβάζει ένα αντίγραφο και επιστρέφει ένα λεξικό με όσα βρήκε."""
    tables = {}          # όνομα πίνακα -> πόσες γραμμές δεδομένων έχει το αντίγραφο
    current = None       # ο πίνακας του INSERT που διαβάζουμε τώρα
    found = {"drops": 0, "checks": 0, "accounts": 0, "complete": False}
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("CREATE TABLE"):
                tables[line.split("`")[1]] = 0
            elif line.startswith("INSERT INTO"):
                current = line.split("`")[1]
            elif line.startswith("(") and current is not None:
                tables[current] += 1                 # κάθε γραμμή δεδομένων του INSERT αρχίζει με «(»
            elif line.startswith("DROP TABLE IF EXISTS"):
                found["drops"] += 1
            elif line.lstrip().startswith("CONSTRAINT") and "CHECK (" in line:
                found["checks"] += 1
            elif line.startswith("CREATE USER") or line.startswith("GRANT "):
                found["accounts"] += 1
            elif line.startswith("-- Dump completed") or line.strip() == "COMMIT;":
                found["complete"] = True
    found["tables"] = tables
    return found


def show_report(path):
    """Τυπώνει την αναφορά για ένα αντίγραφο."""
    found = inspect(path)
    print()
    print(f"Αρχείο: {path} ({os.path.getsize(path)} bytes)")
    print()
    print("Πίνακες και γραμμές δεδομένων:")
    for name, rows in found["tables"].items():
        print(f"  {name:<16}{rows:>4}")
    print()
    print(f"{'Εντολές DROP TABLE IF EXISTS':<34}{found['drops']}")
    print(f"{'Περιορισμοί CHECK':<34}{found['checks']}")
    print(f"{'Λογαριασμοί (CREATE USER, GRANT)':<34}{found['accounts']}")
    print(f"{'Το αρχείο τελειώνει κανονικά':<34}{'ναι' if found['complete'] else 'ΟΧΙ'}")
    print()
    if not found["complete"]:
        print("ΠΡΟΣΟΧΗ: το αρχείο δεν τελειώνει όπως πρέπει. Το αντίγραφο διακόπηκε στη μέση;")
    if found["checks"] == 0:
        print("ΠΡΟΣΟΧΗ: δεν υπάρχει κανένας περιορισμός CHECK. Μετά την επαναφορά η βάση δεν θα ελέγχει πια τις τιμές (Μάθημα 8).")
    if found["drops"] == 0:
        print("ΠΡΟΣΟΧΗ: δεν υπάρχουν εντολές DROP TABLE. Αν οι πίνακες υπάρχουν ήδη, η επαναφορά θα δώσει σφάλμα #1050.")
    if found["accounts"] == 0:
        print("Σημείωση: οι λογαριασμοί ΔΕΝ είναι στο αντίγραφο (ανήκουν στον εξυπηρετητή). Θα τους φτιάξεις ξανά με το 02-users.sql του Μαθήματος 17.")


def main():
    files = list_backups(config.BACKUP_FOLDER)
    if len(files) == 0:
        print(f"Ο φάκελος {config.BACKUP_FOLDER} δεν έχει αρχεία .sql. Φτιάξε πρώτα ένα αντίγραφο (Στάδια 1-3).")
        return
    print(f"Αντίγραφα στον φάκελο {config.BACKUP_FOLDER}:")
    for number, name in enumerate(files, 1):
        print(f"  {number}. {name}")
    choice = ui.ask_int("Ποιο να ελέγξω; (0 = έξοδος) ", 0, len(files))
    if choice != 0:
        show_report(os.path.join(config.BACKUP_FOLDER, files[choice - 1]))


if __name__ == "__main__":
    main()
