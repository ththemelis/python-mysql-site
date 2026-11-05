"""Έλεγχος της βάσης του project (Μάθημα 19). Δεν χρειάζεται να το αλλάξεις.

Συνδέεται με τη βάση που ορίζει το config.py (DATABASE), με τον λογαριασμό της εφαρμογής σου, και διαβάζει από την information_schema (το «βιβλίο
περιγραφής» που έχει ο εξυπηρετητής για όλες τις βάσεις) πώς είναι φτιαγμένη: πίνακες, κλειδιά, περιορισμοί και δεδομένα. Δεν αλλάζει τίποτα.
Τρέξε το όσες φορές θέλεις, ώσπου να βγουν όλες οι γραμμές [OK].
"""

import re

import mysql.connector

import config
import db

# Οι ελάχιστες απαιτήσεις του project (ο διδάσκων μπορεί να τις αλλάξει)
MIN_TABLES = 4             # πίνακες
MIN_FOREIGN_KEYS = 3       # ξένα κλειδιά
MIN_ROWS = 3               # γραμμές σε ΚΑΘΕ πίνακα
MIN_ROWS_BIGGEST = 10      # γραμμές στον μεγαλύτερο πίνακα (π.χ. τον πίνακα σύνδεσης)
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")      # πεζά λατινικά, αριθμοί και κάτω παύλα

QUERIES = {
    "tables": "SELECT table_name AS tbl FROM information_schema.tables "
              "WHERE table_schema = %s AND table_type = 'BASE TABLE' ORDER BY table_name",
    "columns": "SELECT table_name AS tbl, column_name AS col, data_type, column_default, extra "
               "FROM information_schema.columns WHERE table_schema = %s ORDER BY table_name, ordinal_position",
    "primary": "SELECT table_name AS tbl, column_name AS col FROM information_schema.key_column_usage "
               "WHERE table_schema = %s AND constraint_name = 'PRIMARY' ORDER BY table_name, ordinal_position",
    "foreign": "SELECT table_name AS tbl, constraint_name AS name, column_name AS col, referenced_table_name AS parent "
               "FROM information_schema.key_column_usage "
               "WHERE table_schema = %s AND referenced_table_name IS NOT NULL ORDER BY table_name, constraint_name, ordinal_position",
    "unique": "SELECT table_name AS tbl, constraint_name AS name FROM information_schema.table_constraints "
              "WHERE table_schema = %s AND constraint_type = 'UNIQUE'",
    "check": "SELECT table_name AS tbl, constraint_name AS name FROM information_schema.check_constraints "
             "WHERE constraint_schema = %s",
}


def read_database(connection):
    """Διαβάζει όλα όσα χρειαζόμαστε και τα επιστρέφει σε ένα λεξικό."""
    info = {}
    with connection.cursor(dictionary=True) as cursor:
        for key, sql in QUERIES.items():
            cursor.execute(sql, (config.DATABASE,))
            info[key] = cursor.fetchall()
        # Οι γραμμές κάθε πίνακα. Το όνομα ενός πίνακα δεν γίνεται παράμετρος (%s): έρχεται από την ίδια τη βάση, όχι από τον χρήστη.
        info["rows"] = {}
        for row in info["tables"]:
            cursor.execute(f"SELECT COUNT(*) AS n FROM `{row['tbl']}`")
            info["rows"][row["tbl"]] = cursor.fetchone()["n"]
    return info


def summarize(info):
    """Φτιάχνει από τα ακατέργαστα αποτελέσματα όσα χρειάζονται για την αναφορά και τους ελέγχους."""
    names = [row["tbl"] for row in info["tables"]]
    primary = {name: [] for name in names}
    for row in info["primary"]:
        primary[row["tbl"]].append(row["col"])

    foreign = {name: {} for name in names}              # πίνακας -> {όνομα περιορισμού: [στήλες]}
    related = set()                                     # πίνακες που συνδέονται με άλλους (ως παιδιά ή ως γονείς)
    for row in info["foreign"]:
        foreign[row["tbl"]].setdefault(row["name"], []).append(row["col"])
        related.add(row["tbl"])
        related.add(row["parent"])

    junctions = []                                      # πίνακες σύνδεσης: πρωτεύον κλειδί με 2+ στήλες, ΟΛΕΣ ξένα κλειδιά
    for name in names:
        fk_columns = [col for cols in foreign[name].values() for col in cols]
        if len(primary[name]) >= 2 and all(col in fk_columns for col in primary[name]):
            junctions.append(name)

    defaults = [row for row in info["columns"] if "auto_increment" not in row["extra"].lower()
                and row["column_default"] is not None and row["column_default"] != "NULL"]
    dates = [row for row in info["columns"] if row["data_type"] in ("date", "datetime", "timestamp", "time")]
    return {"names": names, "primary": primary, "foreign": foreign, "related": related, "junctions": junctions,
            "defaults": defaults, "dates": dates}


def print_tables(info, summary):
    print()
    print(f"{'Πίνακας':<18}{'Στήλες':>7}{'Γραμμές':>9}   {'Πρωτεύον κλειδί':<24}{'Ξένα κλειδιά':>13}")
    for name in summary["names"]:
        count = len([row for row in info["columns"] if row["tbl"] == name])
        primary = ", ".join(summary["primary"][name]) or "—"
        print(f"{name:<18}{count:>7}{info['rows'][name]:>9}   {primary:<24}{len(summary['foreign'][name]):>13}")


def run_checks(info, summary):
    """Επιστρέφει λίστα ελέγχων: (τίτλος, πέρασε;, λεπτομέρεια, υπόδειξη αν δεν πέρασε)."""
    names = summary["names"]
    all_foreign = sum(len(constraints) for constraints in summary["foreign"].values())
    no_pk = [name for name in names if len(summary["primary"][name]) == 0]
    few_rows = [name for name in names if info["rows"][name] < MIN_ROWS]
    biggest = max(info["rows"].values()) if names else 0
    alone = [name for name in names if name not in summary["related"]]
    bad_names = [name for name in names if not NAME_PATTERN.match(name)]
    bad_names += [f"{row['tbl']}.{row['col']}" for row in info["columns"] if not NAME_PATTERN.match(row["col"])]

    return [
        (f"Τουλάχιστον {MIN_TABLES} πίνακες", len(names) >= MIN_TABLES, f"({len(names)})",
         f"Έχεις {len(names)}. Σκέψου ποιο «πράγμα» του θέματός σου λείπει από πίνακα."),
        ("Κάθε πίνακας έχει πρωτεύον κλειδί (PRIMARY KEY)", len(no_pk) == 0, "",
         "Χωρίς πρωτεύον κλειδί: " + ", ".join(no_pk)),
        (f"Τουλάχιστον {MIN_FOREIGN_KEYS} ξένα κλειδιά (FOREIGN KEY)", all_foreign >= MIN_FOREIGN_KEYS, f"({all_foreign})",
         "Κάθε σχέση ένα-προς-πολλά θέλει ένα ξένο κλειδί στον πίνακα της πολλαπλής πλευράς."),
        ("Υπάρχει πίνακας σύνδεσης για σχέση πολλά-προς-πολλά", len(summary["junctions"]) >= 1, "(" + ", ".join(summary["junctions"]) + ")",
         "Ένας πίνακας σύνδεσης έχει σύνθετο πρωτεύον κλειδί από δύο στήλες που είναι ΚΑΙ οι δύο ξένα κλειδιά (Μάθημα 14)."),
        ("Υπάρχει περιορισμός UNIQUE", len(info["unique"]) >= 1, f"({len(info['unique'])})",
         "Ποια στήλη δεν επιτρέπεται να έχει την ίδια τιμή δύο φορές (π.χ. τηλέφωνο, κωδικός);"),
        ("Υπάρχει περιορισμός CHECK", len(info["check"]) >= 1, f"({len(info['check'])})",
         "Ποια τιμή δεν επιτρέπεται να είναι αρνητική ή εκτός ορίων; (Μάθημα 8)"),
        ("Υπάρχει στήλη με προεπιλεγμένη τιμή (DEFAULT)", len(summary["defaults"]) >= 1, f"({len(summary['defaults'])})",
         "Ποια στήλη έχει σχεδόν πάντα την ίδια τιμή (π.χ. κατάσταση, ποσότητα 1);"),
        ("Υπάρχει στήλη ημερομηνίας ή ώρας (DATE, DATETIME)", len(summary["dates"]) >= 1, f"({len(summary['dates'])})",
         "Σχεδόν κάθε εφαρμογή θέλει ένα «πότε». Βάλε τη στήλη σε τύπο DATE ή DATETIME, όχι σε κείμενο."),
        (f"Κάθε πίνακας έχει τουλάχιστον {MIN_ROWS} γραμμές δεδομένων", len(few_rows) == 0, "",
         "Λίγες γραμμές: " + ", ".join(f"{name} ({info['rows'][name]})" for name in few_rows)),
        (f"Ο μεγαλύτερος πίνακας έχει τουλάχιστον {MIN_ROWS_BIGGEST} γραμμές", biggest >= MIN_ROWS_BIGGEST, f"({biggest})",
         "Πρόσθεσε περισσότερα δεδομένα στον πίνακα σύνδεσης ή στον πίνακα των κινήσεων."),
        ("Κανένας πίνακας δεν μένει μόνος (όλοι συνδέονται με ξένο κλειδί)", len(alone) == 0, "",
         "Δεν συνδέονται με κανέναν: " + ", ".join(alone)),
        ("Τα ονόματα είναι με πεζά λατινικά, αριθμούς και κάτω παύλα", len(bad_names) == 0, "",
         "Άλλαξε: " + ", ".join(bad_names[:6])),
    ]


def main():
    print(f"Έλεγχος της βάσης «{config.DATABASE}» με τον λογαριασμό «{config.APP_USER}»")
    try:
        connection = db.connect()
    except mysql.connector.Error as error:
        print(f"Δεν μπόρεσα να συνδεθώ: #{error.errno} {error.msg}")
        if error.errno in (1044, 1049):
            print(f"Η βάση «{config.DATABASE}» δεν υπάρχει, ή ο λογαριασμός δεν έχει δικαίωμα σε αυτήν. Έλεγξε:")
            print("  - το DATABASE στο config.py: πρέπει να είναι το όνομα της ΔΙΚΗΣ ΣΟΥ βάσης,")
            print("  - ότι έτρεξες το 01-schema.sql και το 03-account.sql, και ότι το όνομα της βάσης στο GRANT είναι το ίδιο.")
        elif error.errno == 1045:
            print("Λάθος όνομα λογαριασμού ή κωδικός. Έλεγξε το APP_USER στο config.py και τον κωδικό στο config_local.py (το όνομα και ο κωδικός")
            print("πρέπει να είναι όσα έδωσες στο 03-account.sql).")
        else:
            print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel.")
        return

    with connection:
        info = read_database(connection)
    summary = summarize(info)
    if len(summary["names"]) == 0:
        print("Η βάση δεν έχει κανέναν πίνακα ακόμη. Τρέξε πρώτα το 01-schema.sql.")
        return

    print_tables(info, summary)
    print()
    failed = 0
    for title, passed, detail, hint in run_checks(info, summary):
        if not passed:
            failed += 1
        print(f"{'[OK]    ' if passed else '[ΛΑΘΟΣ]'} {title:<62}{detail if passed else ''}")
        if not passed:
            print(f"         → {hint}")
    print()
    if failed == 0:
        print("Όλοι οι έλεγχοι βγήκαν OK. Η βάση σου ικανοποιεί τις απαιτήσεις του project.")
    else:
        print(f"ΛΑΘΟΣ: {failed} απαιτήσεις δεν ικανοποιούνται ακόμη. Διάβασε τα βέλη (→), διόρθωσε και ξανατρέξε.")


if __name__ == "__main__":
    main()
