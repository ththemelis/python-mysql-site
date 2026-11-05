"""Στάδιο 3: αντίγραφο ασφαλείας της βάσης από την Python.

Τρέχει το mariadb-dump (το ίδιο πρόγραμμα που έτρεξες στο τερματικό) με τον λογαριασμό game_reader και γράφει το αντίγραφο στον φάκελο backups,
με όνομα που έχει ημερομηνία και ώρα.

Συμπλήρωσε τα πέντε κενά (____).
"""

import os
import subprocess
from datetime import datetime

import config


def backup_file_name(moment):
    """Το όνομα του αρχείου: η βάση, η ημερομηνία και η ώρα, π.χ. game_library-2026-11-05_14-30.sql.

    Δεν βάζουμε «:» στην ώρα (τα Windows δεν το δέχονται σε όνομα αρχείου). Η σειρά «έτος-μήνας-μέρα» κάνει τα ονόματα να ταξινομούνται και
    χρονολογικά: το τελευταίο στη λίστα είναι το νεότερο αντίγραφο.
    """
    # TODO 1: η μέθοδος του datetime που γράφει την ημερομηνία και την ώρα με μορφή (Μάθημα 9)
    stamp = moment.____("%Y-%m-%d_%H-%M")
    return f"{config.DATABASE}-{stamp}.sql"


def make_backup(folder=config.BACKUP_FOLDER):
    """Φτιάχνει ένα αντίγραφο και επιστρέφει τη διαδρομή του αρχείου. Αν το mariadb-dump αποτύχει, σηκώνει RuntimeError."""
    # TODO 2: φτιάξε τον φάκελο αν δεν υπάρχει (και μην παραπονεθείς αν υπάρχει ήδη)
    os.makedirs(folder, ____=True)
    path = os.path.join(folder, backup_file_name(datetime.now()))

    # Η εντολή που έτρεξες στο τερματικό, σπασμένη σε κομμάτια: το πρώτο είναι το πρόγραμμα, τα υπόλοιπα τα ορίσματά του
    command = [
        config.DUMP_PROGRAM,
        f"--host={config.HOST}",
        f"--user={config.READER_USER}",          # ο λογαριασμός που ΜΟΝΟ διαβάζει: για αντίγραφο αρκεί
        "--default-character-set=utf8mb4",
        "--single-transaction",
        "--databases", config.DATABASE,
        f"--result-file={path}",
    ]

    # Ο κωδικός ΔΕΝ μπαίνει στην εντολή (θα φαινόταν σε όποιον κοιτάξει τη λίστα των διεργασιών): περνά με μεταβλητή περιβάλλοντος
    # TODO 3: ο κωδικός του λογαριασμού που διαβάζει, από το config
    environment = dict(os.environ, MYSQL_PWD=config.____)

    # TODO 4: η συνάρτηση του module subprocess που τρέχει ένα πρόγραμμα και περιμένει να τελειώσει
    result = subprocess.____(command, env=environment, capture_output=True, text=True)

    # TODO 5: ένα πρόγραμμα που τελειώνει ΣΩΣΤΑ επιστρέφει 0· κάθε άλλος αριθμός σημαίνει αποτυχία (το χαρακτηριστικό του result)
    if result.____ != 0:
        if os.path.exists(path):
            os.remove(path)              # ένα μισό αρχείο είναι χειρότερο από κανένα: δεν το αφήνουμε
        raise RuntimeError(result.stderr.strip())
    return path


def main():
    try:
        path = make_backup()
    except FileNotFoundError:
        print(f"Δεν βρέθηκε το πρόγραμμα αντιγράφων: {config.DUMP_PROGRAM}")
        print("Έλεγξε τη διαδρομή (DUMP_PROGRAM στο config.py ή η μεταβλητή περιβάλλοντος DUMP_PROGRAM).")
        return
    except RuntimeError as error:
        print("Το αντίγραφο ΑΠΕΤΥΧΕ:", error)
        return
    print(f"Το αντίγραφο γράφτηκε: {path} ({os.path.getsize(path)} bytes)")
    print("Έλεγξέ το με: python check_backup.py")


if __name__ == "__main__":
    main()
