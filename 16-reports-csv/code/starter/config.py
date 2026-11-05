"""Οι ρυθμίσεις σύνδεσης με τη βάση.

Ό,τι αλλάζει από υπολογιστή σε υπολογιστή (εξυπηρετητής, χρήστης, κωδικός, βάση) γράφεται εδώ και ΜΟΝΟ εδώ.
Τα άλλα modules διαβάζουν τις τιμές από το config.
"""

import os

# Η os.environ.get("ΟΝΟΜΑ", προεπιλογή) διαβάζει μια ΜΕΤΑΒΛΗΤΗ ΠΕΡΙΒΑΛΛΟΝΤΟΣ: μια ρύθμιση που ορίζεται έξω από το
# πρόγραμμα, στο λειτουργικό σύστημα. Αν δεν υπάρχει, παίρνεις την προεπιλογή.

HOST = os.environ.get("DB_HOST", "localhost")
USER = os.environ.get("DB_USER", "root")
PASSWORD = os.environ.get("DB_PASSWORD", "")
DATABASE = os.environ.get("DB_NAME", "game_library")
