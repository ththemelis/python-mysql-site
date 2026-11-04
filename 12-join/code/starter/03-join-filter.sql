-- Στάδιο 2 — JOIN με φίλτρα, ταξινόμηση και δύο συνηθισμένα λάθη.
--
-- Πριν αρχίσεις: η βάση πρέπει να είναι όπως την άφησε το 01-start-state.sql. Τα ερωτήματα αυτού του σταδίου δεν
-- αλλάζουν δεδομένα.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα.

-- Ερώτημα 1: τα παιχνίδια του είδους «Παζλ» (με το ΟΝΟΜΑ του είδους, όχι με το id) που κοστίζουν λιγότερο από 3 €,
-- φθηνότερα πρώτα
SELECT g.title, g.price
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id
WHERE ge.name = '____' AND g.price < ____
ORDER BY g.price;

-- Ερώτημα 2 (έτοιμο): ΛΑΘΟΣ, ΧΩΡΙΣ ΣΦΑΛΜΑ. Εδώ ο όρος ON ζευγαρώνει το id του παιχνιδιού με το id του είδους.
-- Πόσες γραμμές περιμένεις; Πόσες βγαίνουν;
SELECT g.id, g.title, ge.name
FROM games AS g
JOIN genres AS ge ON g.id = ge.id;

-- Ερώτημα 3: διόρθωσε τον όρο ON: το παιχνίδι ζευγαρώνει με το είδος του μέσω του ξένου κλειδιού
SELECT g.id, g.title, ge.name
FROM games AS g
JOIN genres AS ge ON g.____ = ge.id;

-- Ερώτημα 4 (έτοιμο): ΑΛΛΟ ΛΑΘΟΣ, ΧΩΡΙΣ ΣΦΑΛΜΑ. Ξέχασες τον όρο ON: κάθε παιχνίδι ζευγαρώνει με ΚΑΘΕ είδος
SELECT COUNT(*) AS rows_n
FROM games
JOIN genres;

-- Ερώτημα 5: οι κριτικές μαζί με τον τίτλο του παιχνιδιού τους. Το ξένο κλειδί του reviews είναι το game_id
SELECT g.title, r.stars, r.comment
FROM reviews AS r
JOIN games AS g ON r.____ = g.id
ORDER BY g.title, r.stars DESC;

-- Ερώτημα 6 (έτοιμο): μόνο οι κριτικές του «Turbo Kart Cup». Το παιχνίδι εμφανίζεται ΜΙΑ φορά για κάθε κριτική του
SELECT g.title, r.stars
FROM reviews AS r
JOIN games AS g ON r.game_id = g.id
WHERE g.title = 'Turbo Kart Cup';
