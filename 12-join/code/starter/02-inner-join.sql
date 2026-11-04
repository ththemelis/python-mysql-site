-- Στάδιο 1 — Το πρώτο JOIN: ονόματα αντί για αριθμούς.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import). Τα ερωτήματα αυτού του σταδίου δεν αλλάζουν δεδομένα.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα.

-- Ερώτημα 1 (έτοιμο): ο games γράφει το είδος κάθε παιχνιδιού ως ΑΡΙΘΜΟ (genre_id). Ποιο είδος είναι το 2;
SELECT id, title, genre_id
FROM games
ORDER BY id
LIMIT 5;

-- Ερώτημα 2 (έτοιμο): τα ονόματα των ειδών βρίσκονται στον άλλο πίνακα
SELECT id, name
FROM genres
ORDER BY id;

-- Ερώτημα 3: το πρώτο JOIN. Κάθε παιχνίδι «ζευγαρώνει» με τη γραμμή του genres που έχει id ίσο με το genre_id του
SELECT games.title, genres.name
FROM games
INNER ____ genres ON games.genre_id = genres.id;

-- Ερώτημα 4: το ίδιο, με ψευδώνυμα πινάκων (g, ge) και ψευδώνυμο στήλης (genre_name)
SELECT g.title, ge.name AS genre_name, g.price
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.____
ORDER BY ge.name, g.title;

-- Ερώτημα 5 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Και οι δύο πίνακες έχουν στήλη id: ποια από τις δύο εννοείς;
SELECT id, title, name
FROM games
JOIN genres ON games.genre_id = genres.id;

-- Ερώτημα 6: διόρθωσε το ερώτημα 5: γράψε μπροστά από το id το ψευδώνυμο του πίνακα games
SELECT ____.id, g.title, ge.name
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id;

-- Ερώτημα 7 (έτοιμο): πόσες γραμμές έχει το αποτέλεσμα του JOIN;
SELECT COUNT(*) AS rows_n
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id;
