"""Δεδομένα των εργαστηρίων των Σταδίων 5 και 6. Δεν χρειάζεται να το αλλάξεις.

Η συνάρτηση reset ξαναφέρνει τους δανεισμούς και τα αντίτυπα στην κατάσταση που τα άφησε το 02-loans.sql, ώστε κάθε εργαστήριο να ξεκινά από τα ίδια
δεδομένα όσες φορές κι αν το τρέξεις.
"""


def reset(connection):
    """4 δανεισμοί (οι 1, 2, 3 ενεργοί, ο 4 επιστραμμένος), Star Dodger με 1 διαθέσιμο αντίτυπο, Pixel Racer με 0, όλα τα άλλα με 2."""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM loans WHERE id > 4")
        cursor.execute("UPDATE loans SET returned_on = NULL WHERE id IN (1, 2, 3)")
        cursor.execute("UPDATE loans SET returned_on = '2026-10-12' WHERE id = 4")
        cursor.execute("UPDATE games SET copies_available = 2")
        cursor.execute("UPDATE games SET copies_available = 1 WHERE id = 1")
        cursor.execute("UPDATE games SET copies_available = 0 WHERE id = 2")
    connection.commit()
