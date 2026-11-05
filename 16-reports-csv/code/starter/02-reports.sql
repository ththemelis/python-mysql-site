-- Στάδιο 1 — Αναφορές με GROUP BY και JOIN.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import). Τα ερωτήματα δεν αλλάζουν δεδομένα.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα και τι αριθμούς θα δώσουν οι συναρτήσεις.

-- Ερώτημα 1 (έτοιμο): πόσα παιχνίδια έχει κάθε είδος; INNER JOIN και GROUP BY με το ΟΝΟΜΑ του είδους.
-- Πόσες γραμμές βγαίνουν; Λείπει κάποιο είδος;
SELECT ge.name AS genre, COUNT(*) AS games_n
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id
GROUP BY ge.id, ge.name
ORDER BY games_n DESC, ge.name;

-- Ερώτημα 2: ΟΛΑ τα είδη, με πλήθος και μέση τιμή. LEFT JOIN από τον πίνακα που κρατάς (genres) και COUNT(g.id) (όχι COUNT(*))
SELECT ge.name AS genre, COUNT(____.id) AS games_n, ROUND(AVG(g.price), 2) AS average
FROM genres AS ge
____ JOIN games AS g ON g.genre_id = ge.id
GROUP BY ge.id, ge.name
ORDER BY games_n DESC, ge.name;

-- Ερώτημα 3: μόνο τα είδη με τουλάχιστον 4 παιχνίδια. Το φίλτρο για ΟΜΑΔΕΣ είναι το HAVING (Μάθημα 10)
SELECT ge.name AS genre, COUNT(g.id) AS games_n
FROM genres AS ge
LEFT JOIN games AS g ON g.genre_id = ge.id
GROUP BY ge.id, ge.name
HAVING COUNT(g.id) >= ____
ORDER BY games_n DESC, ge.name;

-- Ερώτημα 4: βαθμολογία ανά παιχνίδι: πλήθος κριτικών και μέσος όρος αστεριών (ένα δεκαδικό), υψηλότερος πρώτα
SELECT g.title, COUNT(*) AS reviews_n, ROUND(____(r.stars), 1) AS average_stars
FROM games AS g
JOIN reviews AS r ON r.game_id = g.id
GROUP BY g.id, g.title
ORDER BY average_stars DESC, g.title;

-- Ερώτημα 5: πόσα παιχνίδια και ποια μέση τιμή έχει κάθε πλατφόρμα, ΜΑΖΙ με την πλατφόρμα που δεν έχει παιχνίδια:
-- δύο LEFT JOIN, ξεκινώντας από τον πίνακα των πλατφορμών
SELECT p.name AS platform, COUNT(g.id) AS games_n, ROUND(AVG(g.price), 2) AS average
FROM platforms AS p
LEFT JOIN game_platforms AS gp ON gp.platform_id = p.id
LEFT JOIN games AS g ON gp.game_id = ____.id
GROUP BY p.id, p.name
ORDER BY games_n DESC, p.name;

-- Ερώτημα 6 (έτοιμο): πόση είναι η συνολική τιμή των παιχνιδιών; (το σωστό άθροισμα)
SELECT SUM(price) AS total, COUNT(*) AS games_n
FROM games;

-- Ερώτημα 7 (έτοιμο): ΠΑΓΙΔΑ. Το ίδιο SUM, αλλά μετά από JOIN με τον πίνακα σύνδεσης. Τι έγινε με το άθροισμα; Δες και το rows_n
SELECT SUM(g.price) AS wrong_total, COUNT(*) AS rows_n
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id;
