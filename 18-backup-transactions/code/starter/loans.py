"""Οι δανεισμοί: συναρτήσεις πρόσβασης στη βάση (Στάδιο 6).

Όπως στο Μάθημα 15, οι συναρτήσεις παίρνουν τη σύνδεση και ΕΠΙΣΤΡΕΦΟΥΝ δεδομένα· δεν τυπώνουν και δεν ρωτούν τον χρήστη. Σήμερα προσθέτουμε το νέο στοιχείο:
κάθε αλλαγή που θέλει ΔΥΟ βήματα γίνεται σε ΜΙΑ συναλλαγή, με ένα commit στο τέλος και rollback αν κάτι πάει στραβά.

Συμπλήρωσε τα πέντε κενά (____).
"""

import mysql.connector

# Κάθε παιχνίδι της βιβλιοθήκης έχει 2 αντίτυπα: τα διαθέσιμα συν οι ενεργοί δανεισμοί πρέπει να κάνουν πάντα 2
COPIES = 2


def get_loans(connection, only_active=False):
    """Επιστρέφει τους δανεισμούς: λίστα από λεξικά (id, title, username, loaned_on, returned_on). Αν only_active, μόνο όσοι δεν έχουν επιστραφεί."""
    sql = (
        "SELECT l.id, g.title, m.username, l.loaned_on, l.returned_on "
        "FROM loans AS l "
        "JOIN games AS g ON g.id = l.game_id "
        "JOIN members AS m ON m.id = l.member_id "
    )
    if only_active:
        sql += "WHERE l.returned_on IS NULL "
    sql += "ORDER BY l.id"
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def lend_game(connection, game_id, member_id):
    """Δανείζει ένα παιχνίδι. ΔΥΟ αλλαγές που γίνονται ΜΑΖΙ ή καθόλου: (1) νέα γραμμή στον loans, (2) ένα διαθέσιμο αντίτυπο λιγότερο.

    Επιστρέφει το id του δανεισμού. Αν η βάση δώσει σφάλμα (π.χ. 4025: δεν υπάρχει διαθέσιμο αντίτυπο), ακυρώνει ΟΛΑ και ξαναπετά το σφάλμα.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO loans (game_id, member_id) VALUES (%s, %s)", (game_id, member_id))
            loan_id = cursor.lastrowid
            cursor.execute("UPDATE games SET copies_available = copies_available - 1 WHERE id = %s", (game_id,))
            # TODO 1: οριστικοποίησε ΚΑΙ τις δύο αλλαγές μαζί
            connection.____()
        except mysql.connector.Error:
            # TODO 2: ακύρωσε ό,τι έγινε ως τώρα, ώστε να μη μείνει τίποτα μισό
            connection.____()
            # TODO 3: ξαναπέτα το ίδιο σφάλμα προς τα πάνω (το lending.py ξέρει τι θα πει στον χρήστη)
            ____
    return loan_id


def return_game(connection, loan_id):
    """Επιστροφή παιχνιδιού: βάζει returned_on στον δανεισμό ΚΑΙ ξαναδίνει ένα διαθέσιμο αντίτυπο, ΜΑΖΙ.

    Επιστρέφει True αν έγινε η επιστροφή, ή False αν ο δανεισμός δεν υπάρχει ή έχει ήδη επιστραφεί (και τότε δεν αλλάζει τίποτα).
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("UPDATE loans SET returned_on = CURDATE() WHERE id = %s AND returned_on IS NULL", (loan_id,))
            # TODO 4: πόσες γραμμές άλλαξε το UPDATE; Αν καμία, δεν υπάρχει ενεργός δανεισμός με αυτό το id
            if cursor.____ == 0:
                connection.rollback()
                return False
            cursor.execute(
                "UPDATE games AS g JOIN loans AS l ON l.game_id = g.id "
                "SET g.copies_available = g.copies_available + 1 WHERE l.id = %s",
                (loan_id,),
            )
            # TODO 5: οριστικοποίησε και τις δύο αλλαγές μαζί
            connection.____()
        except mysql.connector.Error:
            connection.rollback()
            raise
    return True


def check_consistency(connection):
    """Βρίσκει τα παιχνίδια που ΔΕΝ βγάζουν λογαριασμό: διαθέσιμα αντίτυπα + ενεργοί δανεισμοί πρέπει να κάνουν COPIES.

    Επιστρέφει λίστα από λεξικά (id, title, copies_available, active_loans). Κενή λίστα = όλα εντάξει.
    """
    sql = (
        "SELECT g.id, g.title, g.copies_available, COUNT(l.id) AS active_loans "
        "FROM games AS g "
        "LEFT JOIN loans AS l ON l.game_id = g.id AND l.returned_on IS NULL "
        "GROUP BY g.id, g.title, g.copies_available "
        "HAVING g.copies_available + COUNT(l.id) <> %s"
    )
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(sql, (COPIES,))
        return cursor.fetchall()
