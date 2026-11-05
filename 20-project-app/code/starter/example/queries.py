"""Οι εντολές SQL της εφαρμογής «pizzeria» (παράδειγμα του Μαθήματος 20).

Όπως στο Μάθημα 15: κάθε συνάρτηση παίρνει τη σύνδεση, κάνει ΜΙΑ δουλειά με τη βάση και ΕΠΙΣΤΡΕΦΕΙ δεδομένα. Δεν τυπώνει τίποτα και δεν ρωτά τον χρήστη (αυτά είναι
δουλειά του ui.py και του app.py). Τα σφάλματα της βάσης ξαναπετιούνται προς τα πάνω. Οι τιμές του χρήστη πάνε ΠΑΝΤΑ ως παράμετροι (%s), ποτέ μέσα στο κείμενο της SQL.
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


# ---------------------------------------------------------------- οι δουλειές της πιτσαρίας
def get_products(connection):
    """Όλα τα προϊόντα, με το όνομα της κατηγορίας τους (JOIN): λίστα από λεξικά id, name, category, price."""
    sql = (
        "SELECT p.id, p.name, c.name AS category, p.price "
        "FROM products AS p JOIN categories AS c ON p.category_id = c.id "
        "ORDER BY c.name, p.name"
    )
    return select_all(connection, sql)


def get_customers(connection):
    """Όλοι οι πελάτες: λίστα από λεξικά id, name, phone, address."""
    return select_all(connection, "SELECT id, name, phone, address FROM customers ORDER BY name")


def find_customer(connection, customer_id):
    """Ο πελάτης με αυτό το id ως λεξικό, ή None αν δεν υπάρχει."""
    return select_one(connection, "SELECT id, name, phone, address FROM customers WHERE id = %s", (customer_id,))


def add_customer(connection, name, phone, address):
    """Προσθέτει έναν πελάτη και επιστρέφει το id του. Αν το τηλέφωνο υπάρχει ήδη, η βάση δίνει σφάλμα 1062 (UNIQUE)."""
    sql = "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)"
    rowcount, customer_id = change(connection, sql, (name, phone, address))
    return customer_id


def add_order(connection, customer_id, items):
    """Καταχωρεί μια παραγγελία ΜΕ τα προϊόντα της, σε ΜΙΑ συναλλαγή (Μάθημα 18). Επιστρέφει το id της παραγγελίας.

    items: λίστα από (id προϊόντος, ποσότητα). Δύο εντολές: ένα INSERT στον orders και ένα executemany στον order_items. Αν κάτι πάει στραβά, γίνεται
    rollback ΚΑΙ για τις δύο και το σφάλμα ξαναπετιέται: ούτε παραγγελία χωρίς προϊόντα ούτε προϊόντα χωρίς παραγγελία. Η ώρα και η κατάσταση ('new')
    μπαίνουν μόνες τους από τα DEFAULT της βάσης.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,))
            order_id = cursor.lastrowid

            rows = []
            for product_id, quantity in items:
                rows.append((order_id, product_id, quantity))
            cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)", rows)

            connection.commit()
        except mysql.connector.Error:
            connection.rollback()
            raise
    return order_id


def set_status(connection, order_id, status):
    """Αλλάζει την κατάσταση μιας παραγγελίας. Επιστρέφει πόσες γραμμές άλλαξαν (0: δεν υπάρχει η παραγγελία ή έχει ήδη αυτή την κατάσταση)."""
    rowcount, last_id = change(connection, "UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
    return rowcount


def get_orders_of_customer(connection, customer_id):
    """Οι παραγγελίες ενός πελάτη, με το σύνολο της καθεμιάς (JOIN τριών πινάκων και SUM): id, ordered_at, status, total."""
    sql = (
        "SELECT o.id, o.ordered_at, o.status, SUM(oi.quantity * p.price) AS total "
        "FROM orders AS o "
        "JOIN order_items AS oi ON oi.order_id = o.id "
        "JOIN products AS p ON p.id = oi.product_id "
        "WHERE o.customer_id = %s "
        "GROUP BY o.id, o.ordered_at, o.status "
        "ORDER BY o.ordered_at"
    )
    return select_all(connection, sql, (customer_id,))


def revenue_per_category(connection):
    """Τα έσοδα κάθε κατηγορίας (JOIN, GROUP BY, SUM): category, pieces, revenue. Πρώτη η κατηγορία με τα περισσότερα έσοδα."""
    sql = (
        "SELECT ca.name AS category, SUM(oi.quantity) AS pieces, SUM(oi.quantity * p.price) AS revenue "
        "FROM categories AS ca "
        "JOIN products AS p ON p.category_id = ca.id "
        "JOIN order_items AS oi ON oi.product_id = p.id "
        "GROUP BY ca.id, ca.name "
        "ORDER BY revenue DESC"
    )
    return select_all(connection, sql)
