"""Έλεγχος του Σταδίου 3: γράφει ένα δοκιμαστικό αρχείο CSV με ψεύτικα δεδομένα και το διαβάζει πίσω. Δεν συμπληρώνεται."""

from datetime import date
from decimal import Decimal

import export

columns = [("title", "Τίτλος"), ("price", "Τιμή"), ("added_on", "Προστέθηκε"), ("note", "Σχόλιο")]
rows = [
    {"title": "Star Dodger", "price": Decimal("4.99"), "added_on": date(2026, 1, 12), "note": None},
    {"title": "Pixel Racer", "price": Decimal("8.99"), "added_on": date(2026, 1, 12), "note": "Καλό"},
]

count = export.write_csv("report-test.csv", columns, rows)
print("Γράφτηκαν", count, "γραμμές δεδομένων.")

with open("report-test.csv", "rb") as file:
    print("Τα τρία πρώτα bytes του αρχείου:", file.read(3))

with open("report-test.csv", encoding="utf-8-sig") as file:
    for line in file:
        print(line.rstrip())
