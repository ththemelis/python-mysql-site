"""Η ΑΣΦΑΛΗΣ έκδοση του εργαστηρίου SQL injection (Μάθημα 17).

Οι ίδιες δύο συναρτήσεις με το lab_unsafe.py, αλλά οι τιμές του χρήστη δεν μπαίνουν ποτέ στο κείμενο της SQL: στέλνονται χωριστά, ως παράμετροι (%s).
Τρέξε το: python lab_safe.py

Συμπλήρωσε τα τέσσερα κενά (____).
"""

import lab_menu


def login_safe(connection, username, password):
    """Επιστρέφει (id, ρόλος) του μέλους αν τα στοιχεία είναι σωστά, αλλιώς None. Οι τιμές πάνε ως ΠΑΡΑΜΕΤΡΟΙ."""
    sql = "SELECT id, role FROM members WHERE username = %s AND password_hash = SHA2(%s, 256)"
    with connection.cursor() as cursor:
        # TODO 1: οι τιμές που αντικαθιστούν τα δύο %s, με τη σειρά τους (πλειάδα)
        cursor.execute(sql, (username, ____))
        print("SQL που στάλθηκε:", cursor.statement)
        rows = cursor.fetchall()
    if len(rows) > 0:
        return rows[0]
    return None


def search_safe(connection, text):
    """Επιστρέφει τα παιχνίδια (τίτλος, τιμή) που έχουν το text στον τίτλο τους. Το % μπαίνει στην ΤΙΜΗ, όχι στην SQL."""
    # TODO 2: το σύμβολο της παραμέτρου (το ίδιο που χρησιμοποιείς σε κάθε execute)
    sql = "SELECT title, price FROM games WHERE title LIKE ____"
    # TODO 3: η τιμή που έδωσε ο χρήστης, ανάμεσα στα δύο %
    pattern = "%" + ____ + "%"
    with connection.cursor() as cursor:
        # TODO 4: η τιμή της παραμέτρου, ως πλειάδα με ένα στοιχείο
        cursor.execute(sql, (____,))
        print("SQL που στάλθηκε:", cursor.statement)
        return cursor.fetchall()


if __name__ == "__main__":
    lab_menu.run("ΑΣΦΑΛΗΣ ΕΚΔΟΣΗ", login_safe, search_safe)
