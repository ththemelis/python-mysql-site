-- Στάδιο 2 — Μια στήλη ημερομηνίας στον πίνακα games.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import), ώστε ο games να έχει 14 γραμμές.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--      (Το ερώτημα 3 είναι ομάδα εντολών: τρέξ' το όλο μαζί.)
--   3. ΠΡΩΤΑ πρόβλεψε αν η εντολή θα πετύχει, τι θα δείξει, ή αν θα δώσει σφάλμα.

-- Ερώτημα 1: νέα στήλη που θα δείχνει ΠΟΤΕ προστέθηκε κάθε παιχνίδι στη βιβλιοθήκη
ALTER TABLE games ADD added_on ____ NULL;

-- Ερώτημα 2: δώσε ημερομηνία στο παιχνίδι 1 (12 Ιανουαρίου 2026, γραμμένη ΕΕΕΕ-ΜΜ-ΗΗ μέσα σε εισαγωγικά)
UPDATE games SET added_on = '____' WHERE id = 1;

-- Ερώτημα 3 (έτοιμο): οι ημερομηνίες των υπόλοιπων παιχνιδιών, όλες μαζί
UPDATE games SET added_on = '2026-01-12' WHERE id = 2;
UPDATE games SET added_on = '2026-02-03' WHERE id = 3;
UPDATE games SET added_on = '2026-03-18' WHERE id = 4;
UPDATE games SET added_on = '2026-04-05' WHERE id = 5;
UPDATE games SET added_on = '2026-05-21' WHERE id = 6;
UPDATE games SET added_on = '2026-06-30' WHERE id = 7;
UPDATE games SET added_on = '2026-07-14' WHERE id = 8;
UPDATE games SET added_on = '2026-08-09' WHERE id = 9;
UPDATE games SET added_on = '2026-09-01' WHERE id = 10;
UPDATE games SET added_on = '2026-09-15' WHERE id = 11;
UPDATE games SET added_on = '2026-10-02' WHERE id = 14;
UPDATE games SET added_on = '2026-10-20' WHERE id = 15;
UPDATE games SET added_on = '2026-10-28' WHERE id = 16;

-- Ερώτημα 4: τώρα όλα έχουν ημερομηνία. Η στήλη δεν θα επιτρέπει πια κενό, και ένα νέο παιχνίδι
-- που δεν θα πάρει ημερομηνία θα παίρνει τη σημερινή
ALTER TABLE games MODIFY added_on DATE NOT NULL ____ (CURDATE());

-- Ερώτημα 5 (έτοιμο): πρόσθεσε ένα παιχνίδι ΧΩΡΙΣ ημερομηνία και δες τι πήρε
INSERT INTO games (title, genre, release_year, price)
VALUES ('Quiz Master', 'Παζλ', 2026, 2.49);

SELECT id, title, added_on
FROM games
WHERE title = 'Quiz Master';

-- Ερώτημα 6: ποια παιχνίδια προστέθηκαν τον Σεπτέμβριο του 2026;
SELECT id, title, added_on
FROM games
WHERE added_on ____ '2026-09-01' AND '2026-09-30';

-- Ερώτημα 7: τα τρία πιο πρόσφατα (εκτός από το Quiz Master), πρώτα το πιο πρόσφατο, με ελληνική μορφή
SELECT title, DATE_FORMAT(added_on, '%d/%m/%Y') AS added
FROM games
WHERE title <> 'Quiz Master'
ORDER BY added_on ____
LIMIT 3;

-- Ερώτημα 8 (έτοιμο): πόσες ημέρες πριν από τις 31/12/2026 προστέθηκε το κάθε παιχνίδι;
SELECT title, added_on, DATEDIFF('2026-12-31', added_on) AS days
FROM games
WHERE title <> 'Quiz Master'
ORDER BY days
LIMIT 3;

-- Ερώτημα 9 (έτοιμο): ΠΡΟΣΟΧΗ. Μια ΑΚΥΡΗ ημερομηνία: η 30 Φεβρουαρίου. Θα δώσει σφάλμα;
INSERT INTO games (title, genre, release_year, price, added_on)
VALUES ('Παιχνίδι με λάθος ημερομηνία', 'Παζλ', 2026, 1.99, '2026-02-30');

-- Ερώτημα 10 (έτοιμο): τι αποθηκεύτηκε;
SELECT id, title, added_on
FROM games
WHERE title = 'Παιχνίδι με λάθος ημερομηνία';

-- Ερώτημα 11 (έτοιμο): καθάρισε το παιχνίδι με τη λάθος ημερομηνία
DELETE FROM games
WHERE title = 'Παιχνίδι με λάθος ημερομηνία';

-- Ερώτημα 12 (έτοιμο): ο περιορισμός CHECK του Μαθήματος 8, για ημερομηνίες από το 2020 και μετά
ALTER TABLE games ADD CONSTRAINT chk_added CHECK (added_on >= '2020-01-01');

-- Ερώτημα 13 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Η ίδια εισαγωγή του ερωτήματος 9, τώρα που υπάρχει ο περιορισμός
INSERT INTO games (title, genre, release_year, price, added_on)
VALUES ('Παιχνίδι με λάθος ημερομηνία', 'Παζλ', 2026, 1.99, '2026-02-30');
