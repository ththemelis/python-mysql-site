"""Στάδιο 4 — Η συνάρτηση ask_date: ρωτά ώσπου να πάρει έγκυρη ημερομηνία.

Η ask_date μοιάζει με την ask_int του Μαθήματος 8, αλλά διαβάζει ημερομηνίες ΗΗ/ΜΜ/ΕΕΕΕ. Παίρνει και μία
ΠΡΟΕΠΙΛΕΓΜΕΝΗ τιμή (default): αν ο χρήστης πατήσει μόνο Enter, επιστρέφεται αυτή.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

from datetime import date, datetime


def ask_date(message, earliest, latest, default=None):
    """Ρωτά ώσπου ο χρήστης να γράψει έγκυρη ημερομηνία ΗΗ/ΜΜ/ΕΕΕΕ από earliest έως latest, και την επιστρέφει ως date.

    Αν ο χρήστης πατήσει μόνο Enter και υπάρχει default, επιστρέφει το default.
    """
    while True:
        text = input(message).strip()
        # TODO 1: αν δεν έγραψε τίποτα και υπάρχει προεπιλεγμένη τιμή (δηλαδή το default δεν είναι None)
        if text == "" and default is not ____:
            return default
        try:
            # TODO 2: η strptime είναι μέθοδος της κλάσης datetime
            when = ____.strptime(text, "%d/%m/%Y").date()
            # TODO 3: η ημερομηνία πρέπει να είναι ανάμεσα στο earliest και στο latest (και τα δύο επιτρέπονται)
            if earliest ____ when <= latest:
                return when
            print(f"Η ημερομηνία πρέπει να είναι από {earliest.strftime('%d/%m/%Y')} έως {latest.strftime('%d/%m/%Y')}.")
        # TODO 4: το κείμενο που δεν είναι ημερομηνία δίνει ValueError
        except ____:
            print("Γράψε την ημερομηνία ως ΗΗ/ΜΜ/ΕΕΕΕ, π.χ. 15/09/2026.")


print("=== Δοκιμή της ask_date ===")
first = ask_date("Ημερομηνία (από 01/01/2020 έως σήμερα): ", date(2020, 1, 1), date.today())
print("Πήρα:", first, "|", first.strftime("%d/%m/%Y"))
print()
second = ask_date("Ημερομηνία (Enter για σήμερα): ", date(2020, 1, 1), date.today(), default=date.today())
print("Πήρα:", second)
