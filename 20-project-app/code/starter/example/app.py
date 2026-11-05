"""Η εφαρμογή «Πιτσαρία Φούρνος» (παράδειγμα του Μαθήματος 20). Τρέξε την με: python app.py

Το μενού και η σύνδεση των modules: ρωτά με το ui, μιλά με τη βάση μέσω του queries, και χειρίζεται τα σφάλματα. Κάθε επιλογή του μενού είναι ΜΙΑ συνάρτηση εδώ, που
καλεί ΜΙΑ συνάρτηση του queries (όπως στο Μάθημα 15). Η λίστα OPTIONS στο τέλος του αρχείου δένει τα νούμερα του μενού με τις συναλλαγές.
"""

import mysql.connector

import db
import queries
import ui

TITLE = "ΠΙΤΣΑΡΙΑ ΦΟΥΡΝΟΣ"

STATUSES = ["new", "ready", "delivered"]


def choose_customer(connection):
    """Δείχνει τους πελάτες, ρωτά ποιον και επιστρέφει τον πελάτη (λεξικό), ή None αν δεν υπάρχει πελάτης με αυτό το id."""
    ui.print_table(queries.get_customers(connection), [("id", "Id", 4), ("name", "Όνομα", 22), ("phone", "Τηλέφωνο", 11)])
    customer_id = ui.ask_int("Id πελάτη: ", 1, 1000000)
    customer = queries.find_customer(connection, customer_id)
    if customer is None:
        print("Δεν υπάρχει πελάτης με αυτό το id.")
    return customer


def ask_items(products):
    """Ρωτά ποια προϊόντα και πόσα τεμάχια, ώσπου ο χρήστης να γράψει 0. Επιστρέφει λίστα από (id προϊόντος, ποσότητα)."""
    known = {}                                  # id προϊόντος -> όνομα, για να ελέγχουμε ότι υπάρχει
    for product in products:
        known[product["id"]] = product["name"]

    quantities = {}                             # id προϊόντος -> ποσότητα (το ίδιο προϊόν δύο φορές: αθροίζεται)
    while True:
        product_id = ui.ask_int("Id προϊόντος (0 για τέλος): ", 0, 1000000)
        if product_id == 0:
            break
        if product_id not in known:
            print("Δεν υπάρχει προϊόν με αυτό το id.")
            continue
        quantity = ui.ask_int(f"Πόσα τεμάχια «{known[product_id]}» (1-20): ", 1, 20)
        if product_id in quantities:
            quantities[product_id] += quantity
        else:
            quantities[product_id] = quantity

    items = []
    for product_id in quantities:
        items.append((product_id, quantities[product_id]))
    return items


# ---------------------------------------------------------------- οι επιλογές του μενού
def show_products(connection):
    """Επιλογή 1: εμφανίζει τα προϊόντα με την κατηγορία τους."""
    rows = queries.get_products(connection)
    ui.print_table(rows, [("id", "Id", 4), ("name", "Προϊόν", 20), ("category", "Κατηγορία", 12), ("price", "Τιμή €", 7)])


def add_customer(connection):
    """Επιλογή 2: ζητά τα στοιχεία ενός πελάτη και τον προσθέτει."""
    name = ui.ask_text("Όνομα: ", 60)
    phone = ui.ask_digits("Τηλέφωνο (10 ψηφία): ", 10)
    address = ui.ask_text("Διεύθυνση: ", 100)
    try:
        customer_id = queries.add_customer(connection, name, phone, address)
        print(f"Προστέθηκε ο πελάτης «{name}» με id {customer_id}.")
    except mysql.connector.IntegrityError as error:
        if error.errno == 1062:
            print("Υπάρχει ήδη πελάτης με αυτό το τηλέφωνο. Δεν έγινε καμία αλλαγή.")
        else:
            print("Η βάση δεν δέχτηκε τα δεδομένα:", error.msg)


def new_order(connection):
    """Επιλογή 3: καταχωρεί μια παραγγελία με πολλά προϊόντα (μία συναλλαγή)."""
    customer = choose_customer(connection)
    if customer is None:
        return
    ui.print_table(queries.get_products(connection), [("id", "Id", 4), ("name", "Προϊόν", 20), ("price", "Τιμή €", 7)])
    items = ask_items(queries.get_products(connection))
    if len(items) == 0:
        print("Η παραγγελία δεν έχει προϊόντα. Δεν έγινε καμία αλλαγή.")
        return
    try:
        order_id = queries.add_order(connection, customer["id"], items)
        print(f"Η παραγγελία καταχωρήθηκε (id {order_id}, {len(items)} προϊόντα, πελάτης {customer['name']}).")
    except mysql.connector.IntegrityError as error:
        if error.errno == 1452:
            print("Ο πελάτης ή ένα προϊόν δεν υπάρχει πια. Δεν έγινε καμία αλλαγή.")
        else:
            print("Η βάση δεν δέχτηκε την παραγγελία. Δεν έγινε καμία αλλαγή:", error.msg)


def change_status(connection):
    """Επιλογή 4: αλλάζει την κατάσταση μιας παραγγελίας."""
    order_id = ui.ask_int("Id παραγγελίας: ", 1, 1000000)
    status = ui.ask_choice("Νέα κατάσταση (new, ready, delivered): ", STATUSES)
    changed = queries.set_status(connection, order_id, status)
    if changed == 1:
        print("Η κατάσταση άλλαξε.")
    else:
        print("Δεν άλλαξε τίποτα: δεν υπάρχει η παραγγελία ή έχει ήδη αυτή την κατάσταση.")


def show_orders_of_customer(connection):
    """Επιλογή 5: εμφανίζει τις παραγγελίες ενός πελάτη, με το σύνολο της καθεμιάς."""
    customer = choose_customer(connection)
    if customer is None:
        return
    rows = queries.get_orders_of_customer(connection, customer["id"])
    if len(rows) == 0:
        print(f"Ο πελάτης {customer['name']} δεν έχει παραγγελίες.")
    else:
        print(f"Παραγγελίες του πελάτη {customer['name']}:")
        ui.print_table(rows, [("id", "Id", 4), ("ordered_at", "Πότε", 16), ("status", "Κατάσταση", 10), ("total", "Σύνολο €", 9)])


def show_revenue(connection):
    """Επιλογή 6: εμφανίζει τα έσοδα ανά κατηγορία."""
    rows = queries.revenue_per_category(connection)
    ui.print_table(rows, [("category", "Κατηγορία", 12), ("pieces", "Τεμάχια", 8), ("revenue", "Έσοδα €", 9)])


# Τα νούμερα του μενού, τα κείμενά τους και οι συναρτήσεις που τρέχουν (κλειδί, κείμενο, συνάρτηση)
OPTIONS = [
    ("1", "Εμφάνιση προϊόντων", show_products),
    ("2", "Νέος πελάτης", add_customer),
    ("3", "Νέα παραγγελία (πολλά προϊόντα)", new_order),
    ("4", "Αλλαγή κατάστασης παραγγελίας", change_status),
    ("5", "Παραγγελίες ενός πελάτη", show_orders_of_customer),
    ("6", "Έσοδα ανά κατηγορία", show_revenue),
]


def main():
    try:
        connection = db.connect()
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel, και τα config.py και config_local.py.")
        return

    actions = {}                                # νούμερο μενού -> συνάρτηση
    for key, text, function in OPTIONS:
        actions[key] = function

    with connection:
        while True:
            connection.commit()                 # νέα «φωτογραφία» της βάσης σε κάθε γύρο (Μάθημα 7)
            ui.show_menu(TITLE, OPTIONS)
            choice = input("Επιλογή: ").strip()
            if choice == "0":
                break
            if choice in actions:
                try:
                    actions[choice](connection)
                except mysql.connector.Error as error:
                    print("Σφάλμα της βάσης:", error.msg)
            else:
                print("Γράψε έναν αριθμό από το μενού.")
    print("Γεια σου!")


if __name__ == "__main__":
    main()
