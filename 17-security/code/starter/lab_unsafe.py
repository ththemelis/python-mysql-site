"""ΕΥΠΑΘΗΣ ΕΚΔΟΣΗ για το εργαστήριο SQL injection του Μαθήματος 17. ΜΗΝ γράφεις ΠΟΤΕ έτσι πραγματικό κώδικα.

Οι δύο συναρτήσεις χτίζουν την SQL με f-strings: ό,τι γράφει ο χρήστης μπαίνει ΜΕΣΑ στο κείμενο της εντολής. Το print της SQL υπάρχει μόνο για να τη δεις.
Τρέξε το: python lab_unsafe.py   (πρώτα, το 03-members.sql)
"""

import lab_menu


def login_unsafe(connection, username, password):
    """Επιστρέφει (id, ρόλος) του μέλους αν τα στοιχεία είναι σωστά, αλλιώς None."""
    sql = f"SELECT id, role FROM members WHERE username = '{username}' AND password_hash = SHA2('{password}', 256)"
    print("SQL που στάλθηκε:", sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    if len(rows) > 0:
        return rows[0]
    return None


def search_unsafe(connection, text):
    """Επιστρέφει τα παιχνίδια (τίτλος, τιμή) που έχουν το text στον τίτλο τους."""
    sql = f"SELECT title, price FROM games WHERE title LIKE '%{text}%'"
    print("SQL που στάλθηκε:", sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


if __name__ == "__main__":
    lab_menu.run("ΕΥΠΑΘΗΣ ΕΚΔΟΣΗ", login_unsafe, search_unsafe)
