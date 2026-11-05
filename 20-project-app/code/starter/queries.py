"""Οι εντολές SQL της εφαρμογής σου (Μάθημα 20).

Όπως στο Μάθημα 15: κάθε συνάρτηση παίρνει τη σύνδεση, κάνει ΜΙΑ δουλειά με τη βάση και ΕΠΙΣΤΡΕΦΕΙ δεδομένα. Δεν τυπώνει τίποτα και δεν ρωτά τον χρήστη (αυτά είναι δουλειά
του ui.py και του app.py). Τα σφάλματα της βάσης ξαναπετιούνται προς τα πάνω. Οι τιμές του χρήστη πάνε ΠΑΝΤΑ ως παράμετροι (%s), ποτέ μέσα στο κείμενο της SQL (Μάθημα 17).

Οι τρεις γενικές συναρτήσεις παρακάτω είναι ΕΤΟΙΜΕΣ. Οι δικές σου δουλειές γράφονται μετά, με βάση το παράδειγμα της πιτσαρίας (example/queries.py): η SQL που έγραψες
στο 04-queries.sql του Μαθήματος 19 γίνεται το κείμενο των συναρτήσεων.
"""

import mysql.connector


# ---------------------------------------------------------------- τρεις γενικές συναρτήσεις: οι πρώτες ύλες όλων των άλλων
def select_all(connection, sql, params=()):
    """Τρέχει ένα SELECT και επιστρέφει όλες τις γραμμές ως λίστα από λεξικά (κλειδί = όνομα στήλης ή ψευδώνυμο AS)."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def select_one(connection, sql, params=()):
    """Τρέχει ένα SELECT και επιστρέφει την πρώτη γραμμή ως λεξικό, ή None αν δεν βρέθηκε καμία."""
    rows = select_all(connection, sql, params)
    if len(rows) == 0:
        return None
    return rows[0]


def change(connection, sql, params=()):
    """Τρέχει ένα INSERT, UPDATE ή DELETE, κάνει commit και επιστρέφει (πόσες γραμμές άλλαξαν, id της νέας γραμμής).

    Αν η βάση δώσει σφάλμα, κάνει rollback και ξαναπετά το σφάλμα (δεν μένει τίποτα μισό).
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql, params)
            connection.commit()
            return cursor.rowcount, cursor.lastrowid
        except mysql.connector.Error:
            connection.rollback()
            raise


# ---------------------------------------------------------------- οι δουλειές της εφαρμογής ΣΟΥ
# Γράψε τις συναρτήσεις σου εδώ, μία για κάθε επιλογή του μενού. Σβήσε τα σχόλια του προτύπου όταν γράψεις τη δική σου.

# TODO 1 (Στάδιο 2): μια συνάρτηση που ΔΙΑΒΑΖΕΙ από ΠΟΛΛΟΥΣ πίνακες (JOIN). Πρότυπο:
#
# def get_products(connection):
#     """Όλα τα προϊόντα, με το όνομα της κατηγορίας τους (JOIN): λίστα από λεξικά."""
#     sql = (
#         "SELECT p.id, p.name, c.name AS category, p.price "
#         "FROM products AS p JOIN categories AS c ON p.category_id = c.id "
#         "ORDER BY c.name, p.name"
#     )
#     return select_all(connection, sql)

# TODO 2 (Στάδιο 3): μια συνάρτηση που ΠΡΟΣΘΕΤΕΙ μια γραμμή και επιστρέφει το id της. Πρότυπο:
#
# def add_customer(connection, name, phone, address):
#     """Προσθέτει έναν πελάτη και επιστρέφει το id του. Αν το τηλέφωνο υπάρχει ήδη, η βάση δίνει σφάλμα 1062 (UNIQUE)."""
#     sql = "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)"
#     rowcount, customer_id = change(connection, sql, (name, phone, address))
#     return customer_id

# TODO 3 (Στάδιο 4): μια ΣΥΝΑΛΛΑΓΗ με δύο ή περισσότερες εντολές (π.χ. μια παραγγελία ΜΑΖΙ με τα προϊόντα της), με ένα commit, rollback και raise.
#    Πρότυπο: η add_order στο example/queries.py.

# TODO 4 (Στάδιο 5): μια αναφορά (GROUP BY) ή μια αλλαγή (UPDATE / DELETE). Πρότυπα: revenue_per_category, set_status στο example/queries.py.
