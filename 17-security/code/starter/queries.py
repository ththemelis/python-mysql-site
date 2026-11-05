"""Οι εντολές SQL της εφαρμογής.

Κάθε συνάρτηση παίρνει τη σύνδεση, κάνει ΜΙΑ δουλειά με τη βάση και ΕΠΙΣΤΡΕΦΕΙ δεδομένα. Δεν τυπώνει τίποτα και δεν
ρωτά τον χρήστη: αυτά είναι δουλειά του ui.py και του app.py. Τα σφάλματα της βάσης ξαναπετιούνται προς τα πάνω.
"""

import mysql.connector

# Το κοινό κομμάτι των ερωτημάτων που φέρνουν παιχνίδια, με το όνομα του είδους τους (JOIN με τον genres)
SELECT_GAMES = (
    "SELECT g.id, g.title, ge.name AS genre_name, g.release_year, g.price, g.added_on "
    "FROM games AS g JOIN genres AS ge ON g.genre_id = ge.id "
)


def get_games(connection):
    """Επιστρέφει όλα τα παιχνίδια: λίστα από λεξικά."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(SELECT_GAMES + "ORDER BY g.id")
        return cursor.fetchall()


def search_games(connection, text):
    """Επιστρέφει τα παιχνίδια που ο τίτλος τους περιέχει το text."""
    pattern = "%" + text + "%"
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(SELECT_GAMES + "WHERE g.title LIKE %s ORDER BY g.id", (pattern,))
        return cursor.fetchall()


def games_since(connection, since):
    """Επιστρέφει τα παιχνίδια που προστέθηκαν από την ημερομηνία since (αντικείμενο date) και μετά."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(SELECT_GAMES + "WHERE g.added_on >= %s ORDER BY g.added_on, g.id", (since,))
        return cursor.fetchall()


def get_genres(connection):
    """Επιστρέφει τα είδη: λίστα από λεξικά με κλειδιά id και name."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, name FROM genres ORDER BY id")
        return cursor.fetchall()


def get_platforms(connection):
    """Επιστρέφει τις πλατφόρμες: λίστα από λεξικά με κλειδιά id και name."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, name FROM platforms ORDER BY id")
        return cursor.fetchall()


def find_title(connection, game_id):
    """Επιστρέφει τον τίτλο του παιχνιδιού με αυτό το id, ή None αν δεν υπάρχει τέτοιο παιχνίδι."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT title FROM games WHERE id = %s", (game_id,))
        row = cursor.fetchone()

    if row is None:
        return None
    return row[0]


def add_game(connection, title, genre_id, year, price, description, added_on, platform_ids):
    """Προσθέτει ένα παιχνίδι και τις πλατφόρμες του, με ΕΝΑ commit. Επιστρέφει το id του νέου παιχνιδιού."""
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO games (title, release_year, price, description, added_on, genre_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (title, year, price, description, added_on, genre_id),
            )
            game_id = cursor.lastrowid

            links = []
            for platform_id in platform_ids:
                links.append((game_id, platform_id))
            if len(links) > 0:
                cursor.executemany("INSERT INTO game_platforms (game_id, platform_id) VALUES (%s, %s)", links)

            connection.commit()
        except mysql.connector.Error:
            connection.rollback()               # δεν μένει τίποτα μισό
            raise                                # δεν το «καταπίνουμε»: ο ui/app ξέρουν τι θα πουν στον χρήστη
    return game_id


def change_price(connection, game_id, price):
    """Αλλάζει την τιμή ενός παιχνιδιού. Επιστρέφει πόσες γραμμές άλλαξαν (0: δεν υπάρχει το id ή η τιμή ήταν ήδη αυτή)."""
    with connection.cursor() as cursor:
        cursor.execute("UPDATE games SET price = %s WHERE id = %s", (price, game_id))
        connection.commit()
        return cursor.rowcount


def delete_game(connection, game_id):
    """Σβήνει ένα παιχνίδι μαζί με τις πλατφόρμες του. Επιστρέφει True αν σβήστηκε, αλλιώς False.

    Αν το παιχνίδι έχει κριτικές, η βάση δίνει #1451 και το σφάλμα ξαναπετιέται (οι πλατφόρμες του μένουν, λόγω του rollback).
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM game_platforms WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
            deleted = cursor.rowcount == 1
            if deleted:
                connection.commit()
            else:
                connection.rollback()
        except mysql.connector.Error:
            connection.rollback()
            raise
    return deleted


def get_reviews(connection, game_id):
    """Επιστρέφει τις κριτικές ενός παιχνιδιού: λίστα από λεξικά (title, stars, comment).

    Κενή λίστα: δεν υπάρχει τέτοιο παιχνίδι. Ένα λεξικό με stars ίσο με None: το παιχνίδι δεν έχει κριτικές (LEFT JOIN).
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT g.title, r.stars, r.comment "
            "FROM games AS g LEFT JOIN reviews AS r ON r.game_id = g.id "
            "WHERE g.id = %s ORDER BY r.id",
            (game_id,),
        )
        return cursor.fetchall()


def get_platforms_of_game(connection, game_id):
    """Επιστρέφει ένα λεξικό με title και platforms (οι πλατφόρμες σε ένα κείμενο), ή None αν δεν υπάρχει το παιχνίδι.

    Το platforms είναι None όταν το παιχνίδι δεν έχει καμία πλατφόρμα.
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT g.title, GROUP_CONCAT(p.name ORDER BY p.name SEPARATOR ', ') AS platforms "
            "FROM games AS g "
            "LEFT JOIN game_platforms AS gp ON gp.game_id = g.id "
            "LEFT JOIN platforms AS p ON gp.platform_id = p.id "
            "WHERE g.id = %s "
            "GROUP BY g.id, g.title",
            (game_id,),
        )
        return cursor.fetchone()
