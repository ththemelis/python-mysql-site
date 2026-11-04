-- Στάδιο 2 — Ομάδες: GROUP BY και HAVING.
--
-- Πριν αρχίσεις: ο games πρέπει να έχει 30 γραμμές (01-start-state.sql).
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library.
--   3. ΠΡΩΤΑ πρόβλεψε πόσες γραμμές θα έχει το αποτέλεσμα: ΜΙΑ γραμμή για κάθε ΟΜΑΔΑ.

-- Ερώτημα 1: πόσα παιχνίδια έχει κάθε είδος;
SELECT genre, COUNT(*) AS n
FROM games
GROUP BY ____;

-- Ερώτημα 2: ταξινόμησε: πρώτα τα είδη με τα περισσότερα παιχνίδια, και σε ισοβαθμία αλφαβητικά
SELECT genre, COUNT(*) AS n
FROM games
GROUP BY genre
ORDER BY n ____, genre;

-- Ερώτημα 3 (έτοιμο): μέση τιμή και ακριβότερη τιμή ανά είδος
SELECT genre, ROUND(AVG(price), 2) AS average, MAX(price) AS dearest
FROM games
GROUP BY genre
ORDER BY average DESC;

-- Ερώτημα 4: μόνο τα είδη με ΤΟΥΛΑΧΙΣΤΟΝ 3 παιχνίδια. Το HAVING φιλτράρει ΟΜΑΔΕΣ, αφού υπολογιστούν
SELECT genre, COUNT(*) AS n
FROM games
GROUP BY genre
____ COUNT(*) >= 3;

-- Ερώτημα 5 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Το WHERE φιλτράρει γραμμές ΠΡΙΝ τις ομάδες, άρα δεν μπορεί να δει το COUNT(*)
SELECT genre, COUNT(*) AS n
FROM games
WHERE COUNT(*) >= 3
GROUP BY genre;

-- Ερώτημα 6: και τα δύο μαζί. ΠΡΩΤΑ το WHERE (μόνο παιχνίδια του 2022 και μετά), ΜΕΤΑ οι ομάδες με τουλάχιστον 2 παιχνίδια
SELECT genre, COUNT(*) AS n, ROUND(AVG(price), 2) AS average
FROM games
WHERE release_year ____ 2022
GROUP BY genre
HAVING COUNT(*) >= 2
ORDER BY average DESC;

-- Ερώτημα 7 (έτοιμο): ομάδες ανά χρονιά κυκλοφορίας
SELECT release_year, COUNT(*) AS n
FROM games
GROUP BY release_year
ORDER BY release_year;

-- Ερώτημα 8: ομάδες ανά ΜΗΝΑ προσθήκης (η MONTH είναι από το Μάθημα 9)
SELECT MONTH(added_on) AS month, COUNT(*) AS n
FROM games
GROUP BY ____(added_on)
ORDER BY month;

-- Ερώτημα 9 (έτοιμο): ΠΡΟΣΟΧΗ! Μια στήλη (title) που ΔΕΝ είναι στο GROUP BY και δεν είναι συγκέντρωση.
-- Δεν δίνει σφάλμα. Ποιον τίτλο δείχνει για κάθε είδος;
SELECT genre, title, COUNT(*) AS n
FROM games
GROUP BY genre;
