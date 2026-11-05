"""Ό,τι ρωτά τον χρήστη και ό,τι τυπώνεται στην οθόνη.

Το module δεν ξέρει τίποτα για τη βάση: τα δεδομένα του έρχονται ως παράμετροι (λίστες από λεξικά). Γι' αυτό
μπορείς να το δοκιμάσεις ακόμη και με σβηστή τη MySQL.

Συμπλήρωσε τα πέντε κενά (____).
"""

from datetime import datetime
from decimal import Decimal, InvalidOperation


def show_menu():
    """Εμφανίζει το μενού επιλογών."""
    print()
    print("=== ΒΙΒΛΙΟΘΗΚΗ ΠΑΙΧΝΙΔΙΩΝ ===")
    print("1. Εμφάνιση όλων των παιχνιδιών")
    print("2. Αναζήτηση με τίτλο")
    print("3. Προσθήκη παιχνιδιού")
    print("4. Αλλαγή τιμής")
    print("5. Διαγραφή παιχνιδιού")
    print("6. Προσθήκες από ημερομηνία")
    print("7. Κριτικές ενός παιχνιδιού")
    print("8. Πλατφόρμες ενός παιχνιδιού")
    print("0. Έξοδος")


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
            if low <= number <= high:
                return number
            print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")
        except ValueError:
            print("Γράψε έναν ακέραιο αριθμό.")


def ask_price(message):
    """Ρωτά ώσπου ο χρήστης να γράψει τιμή από 0.01 έως 999.99 (δέχεται και κόμμα) και την επιστρέφει ως Decimal."""
    while True:
        text = input(message).replace(",", ".")
        try:
            price = Decimal(text)
            if Decimal("0.01") <= price <= Decimal("999.99"):
                return price
            print("Η τιμή πρέπει να είναι από 0.01 έως 999.99.")
        except InvalidOperation:
            print("Γράψε έναν αριθμό, π.χ. 3.49.")


def ask_date(message, earliest, latest, default=None):
    """Ρωτά ώσπου ο χρήστης να γράψει έγκυρη ημερομηνία ΗΗ/ΜΜ/ΕΕΕΕ από earliest έως latest, και την επιστρέφει ως date.

    Αν ο χρήστης πατήσει μόνο Enter και υπάρχει default, επιστρέφει το default.
    """
    while True:
        text = input(message).strip()
        if text == "" and default is not None:
            return default
        try:
            when = datetime.strptime(text, "%d/%m/%Y").date()
            if earliest <= when <= latest:
                return when
            print(f"Η ημερομηνία πρέπει να είναι από {earliest.strftime('%d/%m/%Y')} έως {latest.strftime('%d/%m/%Y')}.")
        except ValueError:
            print("Γράψε την ημερομηνία ως ΗΗ/ΜΜ/ΕΕΕΕ, π.χ. 15/09/2026.")


def ask_genre(genres):
    """Δείχνει τα είδη (η λίστα genres από την queries.get_genres) και ρωτά ώσπου ο χρήστης να διαλέξει ένα. Επιστρέφει το id."""
    # Ένα λεξικό «id → όνομα» για τα είδη
    names = {}
    print("Είδη:")
    for genre in genres:
        # TODO 1: προσθέτουμε στο λεξικό names: κλειδί το id του είδους, τιμή το όνομά του
        names[genre["id"]] = genre["____"]
        print(f"  {genre['id']:>2}. {genre['name']}")

    while True:
        genre_id = ask_int("id είδους: ", 1, 100000)
        # TODO 2: ο τελεστής που ελέγχει αν ένα κλειδί υπάρχει στο λεξικό
        if genre_id ____ names:
            print(f"Είδος: {names[genre_id]}")
            return genre_id
        print("Δεν υπάρχει είδος με αυτό το id.")


def ask_platforms(platforms):
    """Δείχνει τις πλατφόρμες (η λίστα platforms από την queries.get_platforms) και ρωτά σε ποιες βγαίνει το παιχνίδι.

    Επιστρέφει λίστα από id (μπορεί να είναι κενή).
    """
    names = {}
    print("Πλατφόρμες:")
    for platform in platforms:
        names[platform["id"]] = platform["name"]
        print(f"  {platform['id']:>2}. {platform['name']}")

    while True:
        text = input("Σε ποιες πλατφόρμες βγαίνει; (αριθμοί με κόμμα, Enter για καμία): ").strip()
        if text == "":
            return []

        chosen = []
        valid = True
        # TODO 3: το κείμενο «1,3» σπάει στα κομμάτια «1» και «3» με τη split (διαχωριστής το κόμμα)
        for part in text.split(____):
            try:
                platform_id = int(part)
            except ValueError:
                valid = False
                break
            # TODO 4: το id πρέπει να υπάρχει στο λεξικό names (το αντίθετο του «in»)
            if platform_id ____ names:
                valid = False
                break
            if platform_id not in chosen:
                chosen.append(platform_id)

        if valid:
            return chosen
        print("Γράψε αριθμούς πλατφορμών από τη λίστα, χωρισμένους με κόμμα (π.χ. 1,3).")


def print_games(rows):
    """Εμφανίζει σε στήλες τα παιχνίδια της λίστας rows (κάθε στοιχείο είναι ένα λεξικό από το SELECT)."""
    print()
    print(f"{'id':>3}  {'Τίτλος':<20} {'Είδος':<14} {'Χρονιά':>6} {'Τιμή':>9}  {'Προστέθηκε':<10}")
    for row in rows:
        # TODO 5: η μέθοδος του date που το κάνει κείμενο με μορφή (Μάθημα 9)
        added = row["added_on"].____("%d/%m/%Y")
        print(f"{row['id']:>3}  {row['title']:<20} {row['genre_name']:<14} {row['release_year']:>6} {row['price']:>7.2f} €  {added:<10}")
    print(f"Γραμμές: {len(rows)}")


def print_reviews(rows):
    """Εμφανίζει τις κριτικές ενός παιχνιδιού. Το rows είναι το αποτέλεσμα της queries.get_reviews."""
    if len(rows) == 0:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    print(f"Κριτικές για το «{rows[0]['title']}»:")
    if rows[0]["stars"] is None:
        print("  Κανείς δεν έγραψε ακόμη κριτική.")
        return

    for row in rows:
        if row["comment"] is None:
            comment = "(χωρίς σχόλιο)"
        else:
            comment = row["comment"]
        print(f"  {'*' * row['stars']:<5}  {comment}")


def print_platforms(row):
    """Εμφανίζει τις πλατφόρμες ενός παιχνιδιού. Το row είναι το αποτέλεσμα της queries.get_platforms_of_game."""
    if row is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
    elif row["platforms"] is None:
        print(f"Το «{row['title']}» δεν έχει δηλωμένη καμία πλατφόρμα.")
    else:
        print(f"Το «{row['title']}» βγαίνει σε: {row['platforms']}")
