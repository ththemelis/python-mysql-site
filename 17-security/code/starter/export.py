"""Εξαγωγή αναφορών σε αρχείο CSV.

Το CSV (comma-separated values) είναι ένα αρχείο κειμένου με πίνακα: μία γραμμή για κάθε γραμμή του πίνακα, και οι στήλες
χωρισμένες με έναν διαχωριστή. Ανοίγει στο Excel και σε κάθε επεξεργαστή κειμένου.
"""

import csv
from datetime import date
from decimal import Decimal


def format_value(value):
    """Μετατρέπει μια τιμή της βάσης σε κείμενο για το CSV και για την οθόνη."""
    if value is None:
        return ""
    if isinstance(value, Decimal):
        # Το ελληνικό Excel θέλει υποδιαστολή κόμμα (3,49) και όχι τελεία (3.49)
        return str(value).replace(".", ",")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return str(value)


def write_csv(path, columns, rows):
    """Γράφει τις γραμμές rows (λίστα από λεξικά) στο αρχείο path, σε μορφή CSV.

    Το columns είναι λίστα από ζεύγη (κλειδί του λεξικού, τίτλος της στήλης). Επιστρέφει πόσες γραμμές δεδομένων γράφτηκαν.
    """
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")

        titles = []
        for key, title in columns:
            titles.append(title)
        writer.writerow(titles)

        for row in rows:
            values = []
            for key, title in columns:
                values.append(format_value(row[key]))
            writer.writerow(values)

    return len(rows)
