"""Ό,τι ρωτά τον χρήστη και ό,τι τυπώνεται στην οθόνη (Μάθημα 20). Έτοιμο: δεν χρειάζεται να το αλλάξεις.

Είναι το ui.py των Μαθημάτων 15–17 σε γενική μορφή: δεν ξέρει τίποτα για τη βάση σου. Οι συναρτήσεις ρωτούν μέχρι να πάρουν σωστή απάντηση (Μάθημα 8), και η
print_table τυπώνει οποιαδήποτε λίστα από λεξικά (όπως τη δίνει ο cursor(dictionary=True), Μάθημα 13) ως πίνακα.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def show_menu(title, options):
    """Εμφανίζει το μενού. Το options είναι λίστα από (κλειδί, κείμενο, συνάρτηση): εδώ χρησιμοποιούνται μόνο το κλειδί και το κείμενο."""
    print()
    print(f"=== {title} ===")
    for key, text, function in options:
        print(f"{key}. {text}")
    print("0. Έξοδος")


def ask_text(message, max_length=100):
    """Ρωτά ώσπου ο χρήστης να γράψει κάτι (όχι κενό, όχι πιο μακρύ από max_length) και επιστρέφει το κείμενο, χωρίς κενά στις άκρες."""
    while True:
        text = input(message).strip()
        if text == "":
            print("Το πεδίο δεν μπορεί να μένει κενό.")
        elif len(text) > max_length:
            print(f"Το κείμενο είναι πολύ μακρύ (το πολύ {max_length} χαρακτήρες).")
        else:
            return text


def ask_int(message, low, high):
    """Ρωτά ώσπου ο χρήστης να γράψει ακέραιο από low έως high, και τον επιστρέφει."""
    while True:
        text = input(message)
        try:
            number = int(text)
        except ValueError:
            print("Γράψε έναν ακέραιο αριθμό.")
            continue
        if low <= number <= high:
            return number
        print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")


def ask_price(message, low, high):
    """Ρωτά ώσπου ο χρήστης να γράψει ποσό (π.χ. 7.50) από low έως high, και το επιστρέφει ως Decimal."""
    while True:
        text = input(message).strip().replace(",", ".")
        try:
            amount = Decimal(text)
            if low <= amount <= high:
                return amount
        except InvalidOperation:
            print("Γράψε ένα ποσό, π.χ. 7.50.")
            continue
        print(f"Το ποσό πρέπει να είναι από {low} έως {high}.")


def ask_choice(message, allowed):
    """Ρωτά ώσπου ο χρήστης να γράψει μία από τις επιτρεπόμενες τιμές (λίστα κειμένων) και την επιστρέφει."""
    while True:
        text = input(message).strip().lower()
        if text in allowed:
            return text
        print("Επιτρεπόμενες τιμές: " + ", ".join(allowed))


def ask_digits(message, length):
    """Ρωτά ώσπου ο χρήστης να γράψει ακριβώς length ψηφία (π.χ. τηλέφωνο των 10 ψηφίων) και τα επιστρέφει ως κείμενο."""
    while True:
        text = input(message).strip()
        if text.isdigit() and len(text) == length:
            return text
        print(f"Γράψε ακριβώς {length} ψηφία, χωρίς κενά.")


def ask_yes_no(message):
    """Ρωτά «ναι» ή «όχι» και επιστρέφει True για «ναι»."""
    while True:
        text = input(message + " (ναι/όχι): ").strip().lower()
        if text in ("ναι", "ν", "yes", "y"):
            return True
        if text in ("όχι", "οχι", "ο", "no", "n"):
            return False
        print("Γράψε ναι ή όχι.")


def text_of(value):
    """Μετατρέπει μια τιμή της βάσης σε κείμενο για την οθόνη: το None γίνεται «—», οι ημερομηνίες γράφονται ΗΗ/ΜΜ/ΕΕΕΕ."""
    if value is None:
        return "—"
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return str(value)


def print_table(rows, columns):
    """Τυπώνει τις γραμμές (λίστα από λεξικά) ως πίνακα. Τα columns είναι λίστα από (κλειδί, τίτλος, πλάτος).

    Οι αριθμοί (int, Decimal) στοιχίζονται δεξιά, τα υπόλοιπα αριστερά. Αν δεν υπάρχουν γραμμές, γράφει «Δεν βρέθηκε τίποτα.».
    """
    if len(rows) == 0:
        print("Δεν βρέθηκε τίποτα.")
        return
    print()
    header = ""
    for key, title, width in columns:
        if isinstance(rows[0][key], (int, Decimal)):
            header += f"{title:>{width}} "          # οι αριθμοί και οι τίτλοι τους στοιχίζονται δεξιά
        else:
            header += f"{title:<{width}} "
    print(header.rstrip())
    for row in rows:
        line = ""
        for key, title, width in columns:
            value = row[key]
            text = text_of(value)
            if isinstance(value, (int, Decimal)):
                line += f"{text:>{width}} "
            else:
                line += f"{text:<{width}} "
        print(line.rstrip())
    print(f"({len(rows)} γραμμές)")
