"""Οι εντολές SQL των αναφορών.

Όπως το queries.py του Μαθήματος 15: κάθε συνάρτηση παίρνει τη σύνδεση και ΕΠΙΣΤΡΕΦΕΙ δεδομένα (λίστα από λεξικά). Δεν τυπώνει
και δεν γράφει αρχεία: αυτά τα κάνουν το export.py και το report.py. Έτσι τα ίδια δεδομένα μπορούν να πάνε και στην οθόνη και σε CSV.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

def games_per_genre(connection):
    """Για κάθε είδος, ΚΑΙ για όσα δεν έχουν παιχνίδια: πλήθος παιχνιδιών και μέση τιμή. Λεξικά: genre, games_n, average."""
    # TODO 1: αποτελέσματα ως λεξικά (το ξέρεις από το Μάθημα 13)
    with connection.cursor(dictionary=____) as cursor:
        cursor.execute(
            "SELECT ge.name AS genre, COUNT(g.id) AS games_n, ROUND(AVG(g.price), 2) AS average "
            "FROM genres AS ge LEFT JOIN games AS g ON g.genre_id = ge.id "
            "GROUP BY ge.id, ge.name ORDER BY games_n DESC, ge.name"
        )
        return cursor.fetchall()


def ratings_per_game(connection, min_reviews):
    """Για κάθε παιχνίδι με τουλάχιστον min_reviews κριτικές: πλήθος κριτικών και μέσος όρος αστεριών.

    Λεξικά: title, reviews_n, average_stars (το average_stars είναι Decimal).
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT g.title, COUNT(*) AS reviews_n, ROUND(AVG(r.stars), 1) AS average_stars "
            "FROM games AS g JOIN reviews AS r ON r.game_id = g.id "
            "GROUP BY g.id, g.title "
            "HAVING COUNT(*) >= %s "
            "ORDER BY average_stars DESC, g.title",
            # TODO 2: η τιμή της παραμέτρου %s του HAVING (πλειάδα με μία τιμή)
            (____,),
        )
        return cursor.fetchall()


def games_per_platform(connection):
    """Για κάθε πλατφόρμα, ΚΑΙ για όσες δεν έχουν παιχνίδια: πλήθος παιχνιδιών και μέση τιμή. Λεξικά: platform, games_n, average."""
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT p.name AS platform, COUNT(g.id) AS games_n, ROUND(AVG(g.price), 2) AS average "
            "FROM platforms AS p "
            "LEFT JOIN game_platforms AS gp ON gp.platform_id = p.id "
            "LEFT JOIN games AS g ON gp.game_id = g.id "
            # TODO 3: ομαδοποίηση με το id και το όνομα της πλατφόρμας
            "GROUP BY p.id, p.____ "
            "ORDER BY games_n DESC, p.name"
        )
        # TODO 4: όλες οι γραμμές ως λίστα (από λεξικά)
        return cursor.____()
