"""Στάδιο 2 — Συναρτήσεις που ρωτούν ώσπου να πάρουν σωστή τιμή.

Οι ask_text, ask_int και ask_price ξαναρωτούν μέχρι ο χρήστης να γράψει έγκυρη τιμή, και τότε την επιστρέφουν.
Στο τέλος του αρχείου υπάρχει ένα μικρό πρόγραμμα που τις δοκιμάζει.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from decimal import Decimal, InvalidOperation


def ask_text(message):
    """Ρωτά ώσπου ο χρήστης να γράψει κάτι (όχι κενό) και επιστρέφει το κείμενο, χωρίς κενά στις άκρες."""
    while True:
        text = input(message).strip()
        if text != "":
            return text
        print("Το πεδίο δεν μπορεί να μένει κενό.")


def ask_int(message, low, high):
    """Ρωτά ώσπου ο χρήστης να γράψει ακέραιο από low έως high, και τον επιστρέφει."""
    while True:
        text = input(message)
        try:
            number = int(text)
            # TODO 1: ο αριθμός πρέπει να είναι ανάμεσα στο low και στο high (και τα δύο επιτρέπονται)
            if low <= number ____ high:
                return number
            print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")
        # TODO 2: η int() δίνει ValueError όταν το κείμενο δεν είναι ακέραιος αριθμός
        except ____:
            print("Γράψε έναν ακέραιο αριθμό.")


def ask_price(message):
    """Ρωτά ώσπου ο χρήστης να γράψει τιμή από 0.01 έως 999.99 (δέχεται και κόμμα) και την επιστρέφει ως Decimal."""
    while True:
        text = input(message).replace(",", ".")
        try:
            price = Decimal(text)
            if Decimal("0.01") <= price <= Decimal("999.99"):
                # TODO 3: επίστρεψε την τιμή
                return ____
            print("Η τιμή πρέπει να είναι από 0.01 έως 999.99.")
        # TODO 4: η Decimal() δίνει InvalidOperation (ΟΧΙ ValueError) όταν το κείμενο δεν είναι αριθμός
        except ____:
            print("Γράψε έναν αριθμό, π.χ. 3.49.")


print("=== Δοκιμή των συναρτήσεων ρωτήματος ===")
title = ask_text("Τίτλος: ")
year = ask_int("Χρονιά (1970 έως 2100): ", 1970, 2100)
price = ask_price("Τιμή (0.01 έως 999.99): ")

print()
print("Πήρα:", title, year, price)
