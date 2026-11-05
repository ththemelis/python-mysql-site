"""Στάδιο 4 — Η εφαρμογή με τις πλατφόρμες.

Δουλεύει ΜΕΤΑ το Στάδιο 3 (ο πίνακας game_platforms υπάρχει και είναι γεμάτος). Η add_game ρωτά και τις πλατφόρμες του
παιχνιδιού και γράφει τον πίνακα σύνδεσης με executemany, ΜΕ ΕΝΑ commit μαζί με το παιχνίδι. Η delete_game σβήνει
πρώτα τις γραμμές σύνδεσης και μετά το παιχνίδι. Η νέα επιλογή 8 δείχνει τις πλατφόρμες ενός παιχνιδιού με GROUP_CONCAT.

Συμπλήρωσε τα έξι κενά (____).
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import mysql.connector


# Η παλαιότερη ημερομηνία προσθήκης που δέχεται η εφαρμογή (το ίδιο όριο έχει και ο περιορισμός CHECK της βάσης)
EARLIEST = date(2020, 1, 1)


def connect():
    """Ανοίγει τη σύνδεση με τη βάση game_library και την επιστρέφει."""
    return mysql.connector.connect(host="localhost", user="root", password="", database="game_library")


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


def print_games(rows):
    """Εμφανίζει σε στήλες τα παιχνίδια της λίστας rows (κάθε στοιχείο είναι ένα λεξικό από το SELECT)."""
    print()
    print(f"{'id':>3}  {'Τίτλος':<20} {'Είδος':<14} {'Χρονιά':>6} {'Τιμή':>9}  {'Προστέθηκε':<10}")
    for row in rows:
        added = row["added_on"].strftime("%d/%m/%Y")
        print(f"{row['id']:>3}  {row['title']:<20} {row['genre_name']:<14} {row['release_year']:>6} {row['price']:>7.2f} €  {added:<10}")
    print(f"Γραμμές: {len(rows)}")


def list_games(connection):
    """Εμφανίζει όλα τα παιχνίδια, με το όνομα του είδους τους (JOIN με τον genres)."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.id, g.title, ge.name AS genre_name, g.release_year, g.price, g.added_on "
        "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
        "ORDER BY g.id"
    )
    rows = cursor.fetchall()
    cursor.close()
    print_games(rows)


def search_games(connection):
    """Ζητά μέρος του τίτλου και εμφανίζει τα παιχνίδια που τον περιέχουν."""
    text = input("Μέρος του τίτλου: ")
    pattern = "%" + text + "%"

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.id, g.title, ge.name AS genre_name, g.release_year, g.price, g.added_on "
        "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
        "WHERE g.title LIKE %s ORDER BY g.id",
        (pattern,),
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        print("Δεν βρέθηκε κανένα παιχνίδι.")
    else:
        print_games(rows)


def ask_genre(connection):
    """Δείχνει τα είδη της βάσης και ρωτά ώσπου ο χρήστης να διαλέξει ένα από αυτά. Επιστρέφει το id του είδους."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM genres ORDER BY id")
    genres = cursor.fetchall()
    cursor.close()

    # Ένα λεξικό «id → όνομα» για τα είδη της βάσης
    names = {}
    print("Είδη:")
    for genre in genres:
        names[genre["id"]] = genre["name"]
        print(f"  {genre['id']:>2}. {genre['name']}")

    while True:
        genre_id = ask_int("id είδους: ", 1, 100000)
        if genre_id in names:
            print(f"Είδος: {names[genre_id]}")
            return genre_id
        print("Δεν υπάρχει είδος με αυτό το id.")


def ask_platforms(connection):
    """Δείχνει τις πλατφόρμες και ρωτά σε ποιες βγαίνει το παιχνίδι. Επιστρέφει λίστα από id (μπορεί να είναι κενή)."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM platforms ORDER BY id")
    platforms = cursor.fetchall()
    cursor.close()

    # Ένα λεξικό «id → όνομα» για τις πλατφόρμες της βάσης
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
        # TODO 1: το κείμενο «1,3» σπάει στα κομμάτια «1» και «3» με τη split (το κόμμα είναι ο διαχωριστής)
        for part in text.split(____):
            try:
                platform_id = int(part)
            except ValueError:
                valid = False
                break
            # TODO 2: το id πρέπει να υπάρχει στο λεξικό names (το «not in» είναι το αντίθετο του «in»)
            if platform_id ____ names:
                valid = False
                break
            if platform_id not in chosen:       # κάθε πλατφόρμα μία φορά: το ζευγάρι (game_id, platform_id) είναι πρωτεύον κλειδί
                chosen.append(platform_id)

        if valid:
            return chosen
        print("Γράψε αριθμούς πλατφορμών από τη λίστα, χωρισμένους με κόμμα (π.χ. 1,3).")


def add_game(connection):
    """Ζητά τα στοιχεία ενός παιχνιδιού και των πλατφορμών του (με έλεγχο) και τα προσθέτει στη βάση."""
    title = ask_text("Τίτλος: ")
    genre_id = ask_genre(connection)
    year = ask_int("Χρονιά (1970 έως 2100): ", 1970, 2100)
    price = ask_price("Τιμή (0.01 έως 999.99): ")
    description = input("Περιγραφή (Enter για καμία): ").strip()
    if description == "":
        description = None          # το None της Python γίνεται NULL στη βάση
    added_on = ask_date(
        "Ημερομηνία προσθήκης (ΗΗ/ΜΜ/ΕΕΕΕ, Enter για σήμερα): ", EARLIEST, date.today(), default=date.today()
    )
    platform_ids = ask_platforms(connection)

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO games (title, release_year, price, description, added_on, genre_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, year, price, description, added_on, genre_id),
        )
        game_id = cursor.lastrowid          # το id του νέου παιχνιδιού (πριν από την επόμενη εντολή)

        # Ένα ζευγάρι (game_id, platform_id) για κάθε πλατφόρμα που διάλεξε ο χρήστης
        links = []
        for platform_id in platform_ids:
            links.append((game_id, platform_id))
        if len(links) > 0:
            # TODO 3: ΜΙΑ εντολή για όλα τα ζευγάρια της λίστας (όπως στο Μάθημα 5)
            cursor.____("INSERT INTO game_platforms (game_id, platform_id) VALUES (%s, %s)", links)

        connection.commit()                 # ΕΝΑ commit: το παιχνίδι και οι πλατφόρμες του μπαίνουν μαζί
        print(f"Προστέθηκε το «{title}» με id {game_id} και {len(links)} πλατφόρμες.")
    except mysql.connector.IntegrityError as error:
        connection.rollback()               # αν κάτι αποτύχει, δεν μένει τίποτα μισό
        if error.errno == 1062:
            print(f"Υπάρχει ήδη παιχνίδι με τίτλο «{title}».")
        elif error.errno == 1452:
            print("Το είδος ή η πλατφόρμα που διάλεξες δεν υπάρχει.")
        else:
            print("Η βάση δεν δέχτηκε τα δεδομένα:", error.msg)
    cursor.close()


def change_price(connection):
    """Ζητά το id ενός παιχνιδιού και τη νέα τιμή του (με έλεγχο), και αλλάζει την τιμή."""
    game_id = ask_int("id παιχνιδιού: ", 1, 100000)
    price = ask_price("Νέα τιμή (0.01 έως 999.99): ")

    cursor = connection.cursor()
    cursor.execute("UPDATE games SET price = %s WHERE id = %s", (price, game_id))
    connection.commit()

    if cursor.rowcount == 0:
        print("Δεν άλλαξε καμία γραμμή: ή δεν υπάρχει τέτοιο id ή η τιμή ήταν ήδη αυτή.")
    else:
        print(f"Η τιμή του παιχνιδιού με id {game_id} έγινε {price} €.")
    cursor.close()


def find_title(connection, game_id):
    """Επιστρέφει τον τίτλο του παιχνιδιού με το id που δόθηκε, ή None αν δεν υπάρχει τέτοιο παιχνίδι."""
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM games WHERE id = %s", (game_id,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None
    return row[0]


def delete_game(connection):
    """Ζητά ένα id, δείχνει τον τίτλο, ζητά επιβεβαίωση και σβήνει το παιχνίδι μαζί με τις πλατφόρμες του (όχι αν έχει κριτικές)."""
    game_id = ask_int("id παιχνιδιού που θα σβηστεί: ", 1, 100000)

    title = find_title(connection, game_id)
    if title is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
        return

    answer = input(f"Να σβηστεί το «{title}»; (ναι/όχι): ")
    if answer != "ναι":
        print("Ακυρώθηκε. Δεν σβήστηκε τίποτα.")
        return

    cursor = connection.cursor()
    try:
        # TODO 4: πρώτα σβήνονται οι γραμμές σύνδεσης του παιχνιδιού (πίνακας game_platforms), και μετά το ίδιο το παιχνίδι
        cursor.execute("DELETE FROM ____ WHERE game_id = %s", (game_id,))
        cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
        if cursor.rowcount == 1:
            connection.commit()
            print("Το παιχνίδι σβήστηκε.")
        else:
            connection.rollback()
            print("Κάτι πήγε στραβά. Δεν άλλαξε τίποτα.")
    except mysql.connector.IntegrityError as error:
        connection.rollback()               # ακυρώνει και τον DELETE των γραμμών σύνδεσης: μένει όλο όπως ήταν
        if error.errno == 1451:
            print("Το παιχνίδι έχει κριτικές και δεν μπορεί να σβηστεί. Σβήσε πρώτα τις κριτικές του.")
        else:
            print("Η βάση δεν δέχτηκε την αλλαγή:", error.msg)
    cursor.close()


def games_since(connection):
    """Ζητά μια ημερομηνία και εμφανίζει τα παιχνίδια που προστέθηκαν από εκείνη την ημέρα και μετά."""
    since = ask_date("Από ημερομηνία (ΗΗ/ΜΜ/ΕΕΕΕ): ", EARLIEST, date.today())

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.id, g.title, ge.name AS genre_name, g.release_year, g.price, g.added_on "
        "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
        "WHERE g.added_on >= %s ORDER BY g.added_on, g.id",
        (since,),
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        print("Κανένα παιχνίδι δεν προστέθηκε από εκείνη την ημερομηνία.")
    else:
        print_games(rows)


def show_reviews(connection, game_id):
    """Εμφανίζει τις κριτικές ενός παιχνιδιού. Το LEFT JOIN κρατά το παιχνίδι ακόμη κι αν δεν έχει καμία κριτική."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.title, r.stars, r.comment "
        "FROM games AS g "
        "LEFT JOIN reviews AS r ON r.game_id = g.id "
        "WHERE g.id = %s ORDER BY r.id",
        (game_id,),
    )
    rows = cursor.fetchall()
    cursor.close()

    # Καμία γραμμή: δεν υπάρχει παιχνίδι με αυτό το id
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


def reviews_of_game(connection):
    """Ζητά ένα id και εμφανίζει τις κριτικές του παιχνιδιού."""
    game_id = ask_int("id παιχνιδιού: ", 1, 100000)
    show_reviews(connection, game_id)


def show_platforms(connection, game_id):
    """Εμφανίζει τις πλατφόρμες ενός παιχνιδιού σε μία γραμμή (GROUP_CONCAT)."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT g.title, GROUP_CONCAT(p.name ORDER BY p.name SEPARATOR ', ') AS platforms "
        "FROM games AS g "
        "LEFT JOIN game_platforms AS gp ON gp.game_id = g.id "
        "LEFT JOIN platforms AS p ON gp.platform_id = p.id "
        "WHERE g.id = %s "
        "GROUP BY g.id, g.title",
        (game_id,),
    )
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        print("Δεν υπάρχει παιχνίδι με αυτό το id.")
    # TODO 5: αν το παιχνίδι δεν έχει καμία πλατφόρμα, η GROUP_CONCAT δίνει NULL, δηλαδή None στην Python
    elif row["platforms"] is ____:
        print(f"Το «{row['title']}» δεν έχει δηλωμένη καμία πλατφόρμα.")
    else:
        print(f"Το «{row['title']}» βγαίνει σε: {row['platforms']}")


def platforms_of_game(connection):
    """Ζητά ένα id και εμφανίζει τις πλατφόρμες του παιχνιδιού."""
    game_id = ask_int("id παιχνιδιού: ", 1, 100000)
    show_platforms(connection, game_id)


def main():
    """Το κύριο πρόγραμμα: ανοίγει τη σύνδεση και τρέχει το μενού ώσπου ο χρήστης να διαλέξει έξοδο."""
    try:
        connection = connect()
    except mysql.connector.Error as error:
        print("Δεν μπόρεσα να συνδεθώ με τη βάση:", error.msg)
        print("Έλεγξε ότι η MySQL τρέχει στο XAMPP Control Panel.")
        return

    while True:
        try:
            if not connection.is_connected():
                print("Χάθηκε η σύνδεση με τη βάση. Η εφαρμογή τερματίζεται.")
                break
            # Τελειώνει κάθε ανοιχτή συναλλαγή, ώστε η εφαρμογή να βλέπει τα τελευταία δεδομένα της βάσης
            connection.commit()
            show_menu()
            choice = input("Επιλογή: ")

            if choice == "1":
                list_games(connection)
            elif choice == "2":
                search_games(connection)
            elif choice == "3":
                add_game(connection)
            elif choice == "4":
                change_price(connection)
            elif choice == "5":
                delete_game(connection)
            elif choice == "6":
                games_since(connection)
            elif choice == "7":
                reviews_of_game(connection)
            # TODO 6: η επιλογή 8 εμφανίζει τις πλατφόρμες ενός παιχνιδιού (η επιλογή είναι κείμενο, όπως οι άλλες)
            elif choice == "____":
                platforms_of_game(connection)
            elif choice == "0":
                break
            else:
                print("Άγνωστη επιλογή. Γράψε έναν από τους αριθμούς του μενού.")
        except mysql.connector.Error as error:
            print("Σφάλμα της βάσης:", error.msg)

    connection.close()
    print("Γεια σου!")


main()
