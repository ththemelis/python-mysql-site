"""Στάδιο 4 — Ερωτήματα από την Python.

Το πρόγραμμα ορίζει μία συνάρτηση, τη show, που στέλνει ένα ερώτημα στη βάση και εμφανίζει το αποτέλεσμα σε
πίνακα. Μετά την καλεί έξι φορές, με έξι διαφορετικά ερωτήματα SQL: ο ίδιος κώδικας, διαφορετικά ερωτήματα.

Συμπλήρωσε τα οκτώ κενά (____) μέσα στα ερωτήματα SQL.
"""

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "game_library"


def show(cursor, title, sql):
    """Στέλνει το ερώτημα sql και εμφανίζει το αποτέλεσμα κάτω από τον τίτλο title."""
    cursor.execute(sql)
    rows = cursor.fetchall()

    print()
    print(title)
    print("-" * len(title))
    print(" | ".join(cursor.column_names))
    for row in rows:
        texts = []
        for value in row:
            texts.append(str(value))
        print(" | ".join(texts))
    print(f"Γραμμές: {len(rows)}")


connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = connection.cursor()

# TODO 1: η συνθήκη: τα παιχνίδια που κυκλοφόρησαν το 2023
show(cursor, "Παιχνίδια του 2023", """
    SELECT title, price
    FROM games
    WHERE ____
""")

# TODO 2: ταξινόμηση κατά τιμή (από το φθηνότερο)
show(cursor, "Φθηνά παιχνίδια (έως 8 €)", """
    SELECT title, price
    FROM games
    WHERE price <= 8
    ORDER BY ____
""")

# TODO 3: τα τρία ακριβότερα: φθίνουσα σειρά και όριο γραμμών (δύο κενά)
show(cursor, "Τα τρία ακριβότερα", """
    SELECT title, price
    FROM games
    ORDER BY price ____
    LIMIT ____
""")

# TODO 4: τίτλοι που περιέχουν τη λέξη «Kart» ή τη λέξη «Soccer» (δύο κενά, με μοτίβα LIKE)
show(cursor, "Kart ή Soccer", """
    SELECT title, genre
    FROM games
    WHERE title LIKE ____ OR title LIKE ____
""")

# TODO 5: είδος ανάμεσα σε μια λίστα τιμών, και δεύτερο κριτήριο ταξινόμησης (δύο κενά)
show(cursor, "Αγωνιστικά και αθλητικά", """
    SELECT title, genre, release_year
    FROM games
    WHERE genre ____ ('Αγωνιστικό', 'Αθλητικό')
    ORDER BY release_year, ____
""")

# Ερώτημα 6 (έτοιμο): ερώτημα σε άλλον πίνακα. Η ίδια συνάρτηση, άλλα δεδομένα.
show(cursor, "Πλατφόρμες από το 2020", """
    SELECT name, maker
    FROM platforms
    WHERE release_year >= 2020
    ORDER BY name
""")

cursor.close()
connection.close()
