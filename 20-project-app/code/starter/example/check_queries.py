"""Έλεγχος του queries.py της πιτσαρίας (Μάθημα 20). Τρέχει τις συναρτήσεις του με την πραγματική βάση και δείχνει αν δουλεύουν.

Είναι το «έλεγχος της στρώσης δεδομένων» που ξέρεις από το Μάθημα 15, χωρίς να περάσει από το μενού: εύκολο να ξανατρέχει όσες φορές θέλεις. Ανοίγει ΔΥΟ συνδέσεις: η μία κάνει
τις κινήσεις και η άλλη βλέπει μόνο ό,τι έχει οριστικοποιηθεί (Μάθημα 18). Πριν και μετά σβήνει ό,τι πρόσθεσε το ίδιο, ώστε η βάση να μένει όπως ήταν.
"""

import mysql.connector

import db
import queries

wrong = 0


def check(title, ok, hint=""):
    """Τυπώνει το αποτέλεσμα ενός ελέγχου. Η υπόδειξη φαίνεται μόνο όταν ο έλεγχος αποτύχει."""
    global wrong
    if not ok:
        wrong += 1
    print(f"{title:<66}{'OK' if ok else 'ΛΑΘΟΣ' + ('  ' + hint if hint else '')}")


COUNTS = {
    "orders": "SELECT COUNT(*) AS n FROM orders",
    "order_items": "SELECT COUNT(*) AS n FROM order_items",
}


def count(connection, table):
    """Πόσες γραμμές έχει ο πίνακας (orders ή order_items), όπως τις βλέπει αυτή η σύνδεση. Το rollback ξεκινά νέα «φωτογραφία»: βλέπουμε ό,τι έχει οριστικοποιηθεί."""
    connection.rollback()
    return queries.select_one(connection, COUNTS[table])["n"]


def clean(connection):
    """Σβήνει ό,τι πρόσθεσαν οι έλεγχοι (πελάτες με id > 6, παραγγελίες με id > 10) και ξαναβάζει τις καταστάσεις των παραγγελιών 9 και 10."""
    queries.change(connection, "DELETE FROM order_items WHERE order_id > 10")
    queries.change(connection, "DELETE FROM orders WHERE id > 10")
    queries.change(connection, "DELETE FROM customers WHERE id > 6")
    queries.change(connection, "UPDATE orders SET status = 'new' WHERE id IN (9, 10)")


worker = db.connect()
viewer = db.connect()
clean(worker)

print("--- Προϊόντα")
products = queries.get_products(worker)
check("get_products: 12 προϊόντα", len(products) == 12)
check("το Margherita έχει κατηγορία «Πίτσες» (JOIN)", any(p["name"] == "Margherita" and p["category"] == "Πίτσες" for p in products))

print("--- Πελάτες")
customer_id = queries.add_customer(worker, "Δοκιμαστικός Πελάτης", "6900000099", "Οδός 1")
check("add_customer επέστρεψε id", isinstance(customer_id, int) and customer_id > 6)
check("find_customer τον βρίσκει", queries.find_customer(worker, customer_id)["name"] == "Δοκιμαστικός Πελάτης")
check("find_customer για id που δεν υπάρχει: None", queries.find_customer(worker, 9999) is None)
try:
    queries.add_customer(worker, "Άλλος", "6900000099", "Οδός 2")
    check("το ίδιο τηλέφωνο δεύτερη φορά έπρεπε να δώσει σφάλμα 1062", False, "δεν έγινε σφάλμα")
except mysql.connector.IntegrityError as error:
    check("το ίδιο τηλέφωνο δεύτερη φορά: σφάλμα 1062 (UNIQUE)", error.errno == 1062, f"βγήκε #{error.errno}")

print("--- Παραγγελίες (συναλλαγή)")
orders_before = count(viewer, "orders")
items_before = count(viewer, "order_items")
order_id = queries.add_order(worker, customer_id, [(1, 2), (9, 1)])
check("add_order: η άλλη σύνδεση βλέπει 1 παραγγελία και 2 γραμμές", count(viewer, "orders") == orders_before + 1 and count(viewer, "order_items") == items_before + 2)
order = queries.get_orders_of_customer(worker, customer_id)[0]
check("το σύνολο της παραγγελίας: 2 × 7.50 + 1 × 2.00 = 17.00", str(order["total"]) == "17.00", f"βγήκε {order['total']}")
check("η κατάσταση μπήκε μόνη της (DEFAULT 'new')", order["status"] == "new")

try:
    queries.add_order(worker, customer_id, [(1, 1), (1, 2)])
    check("το ίδιο προϊόν δύο φορές έπρεπε να δώσει σφάλμα 1062", False, "δεν έγινε σφάλμα")
except mysql.connector.IntegrityError as error:
    check("το ίδιο προϊόν δύο φορές στην ίδια παραγγελία: σφάλμα 1062", error.errno == 1062)
check("...και δεν έμεινε μισή παραγγελία (στην ΙΔΙΑ σύνδεση)", count(worker, "orders") == orders_before + 1, "λείπει το rollback;")
worker.commit()
check("...ούτε στην άλλη σύνδεση μετά από ένα commit", count(viewer, "orders") == orders_before + 1 and count(viewer, "order_items") == items_before + 2)

try:
    queries.add_order(worker, 9999, [(1, 1)])
    check("πελάτης που δεν υπάρχει έπρεπε να δώσει σφάλμα 1452", False, "δεν έγινε σφάλμα")
except mysql.connector.IntegrityError as error:
    check("πελάτης που δεν υπάρχει: σφάλμα 1452 (ξένο κλειδί)", error.errno == 1452)
check("...και δεν έμεινε παραγγελία", count(worker, "orders") == orders_before + 1)

print("--- Κατάσταση και έσοδα")
check("set_status(9, 'ready'): άλλαξε 1 γραμμή", queries.set_status(worker, 9, "ready") == 1)
check("το ίδιο ξανά: 0 γραμμές (ήδη 'ready')", queries.set_status(worker, 9, "ready") == 0)
check("παραγγελία που δεν υπάρχει: 0 γραμμές", queries.set_status(worker, 9999, "ready") == 0)
revenue = queries.revenue_per_category(worker)
check("revenue_per_category: 4 κατηγορίες, πρώτες οι Πίτσες", len(revenue) == 4 and revenue[0]["category"] == "Πίτσες")

clean(worker)
worker.close()
viewer.close()

print()
if wrong == 0:
    print("Όλοι οι έλεγχοι βγήκαν όπως αναμενόταν.")
else:
    print(f"ΛΑΘΟΣ: {wrong} έλεγχοι δεν βγήκαν όπως αναμενόταν. Δες το queries.py.")
