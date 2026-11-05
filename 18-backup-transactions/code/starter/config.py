"""Οι ρυθμίσεις του προγράμματος: σύνδεση με τη βάση και αντίγραφα ασφαλείας (Μάθημα 18).

Είναι το config.py του Μαθήματος 17 με ΔΥΟ νέες γραμμές στο τέλος. Ό,τι αλλάζει από υπολογιστή σε υπολογιστή γράφεται εδώ και ΜΟΝΟ εδώ. Οι κωδικοί
έρχονται από το config_local.py, που δεν ανεβαίνει στο git.
"""

import os

# Ο εξυπηρετητής και η βάση αλλάζουν από υπολογιστή σε υπολογιστή: μεταβλητές περιβάλλοντος, όπως στο Μάθημα 15.
HOST = os.environ.get("DB_HOST", "localhost")
DATABASE = os.environ.get("DB_NAME", "game_library")

# Δύο λογαριασμοί, ένας για κάθε δουλειά (η αρχή των ελάχιστων δικαιωμάτων):
APP_USER = "game_app"        # η εφαρμογή: διαβάζει και αλλάζει δεδομένα
READER_USER = "game_reader"  # οι αναφορές και τα αντίγραφα ασφαλείας: μόνο διαβάζουν

# Οι ΚΩΔΙΚΟΙ δεν γράφονται ποτέ εδώ: αυτό το αρχείο ανεβαίνει στο git και το βλέπουν όλοι.
# Ζουν στο config_local.py, ένα αρχείο μόνο στον δικό σου υπολογιστή, που το .gitignore αγνοεί.
try:
    from config_local import APP_PASSWORD, READER_PASSWORD
except ImportError:
    APP_PASSWORD = ""
    READER_PASSWORD = ""

# ΝΕΟ (Μάθημα 18): το πρόγραμμα που φτιάχνει τα αντίγραφα (στο XAMPP βρίσκεται στον φάκελο mysql\bin) και ο φάκελος όπου μπαίνουν.
# Αν το XAMPP δεν είναι στο C:\xampp, όρισε τη μεταβλητή περιβάλλοντος DUMP_PROGRAM με τη σωστή διαδρομή.
DUMP_PROGRAM = os.environ.get("DUMP_PROGRAM", r"C:\xampp\mysql\bin\mariadb-dump.exe")
BACKUP_FOLDER = os.environ.get("BACKUP_FOLDER", "backups")
