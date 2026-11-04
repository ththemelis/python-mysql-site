-- Στάδιο 3 — Το ξένο κλειδί (FOREIGN KEY).
--
-- Πριν αρχίσεις: έχεις κάνει το Στάδιο 2 (ο πίνακας genres υπάρχει και όλα τα παιχνίδια έχουν genre_id).
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε αν η εντολή θα πετύχει ή θα δώσει σφάλμα, και ποιο (#αριθμός).
--   4. Οι εντολές με σημείωση «ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ» το δίνουν επίτηδες.

-- Ερώτημα 1 (έτοιμο): ΠΡΙΝ το ξένο κλειδί: ένα genre_id που δεν υπάρχει (99) γίνεται δεκτό. Τρέξε και τις τρεις εντολές
INSERT INTO games (title, genre, release_year, price, added_on, genre_id)
VALUES ('Παιχνίδι Α', 'Παζλ', 2026, 2.99, '2026-10-30', 99);

SELECT id, title, genre_id
FROM games
WHERE title = 'Παιχνίδι Α';

DELETE FROM games
WHERE title = 'Παιχνίδι Α';

-- Ερώτημα 2: κάθε παιχνίδι ΠΡΕΠΕΙ να έχει είδος: η στήλη δεν θα επιτρέπει πια NULL
ALTER TABLE games MODIFY genre_id INT NOT ____;

-- Ερώτημα 3: το ξένο κλειδί. Η genre_id του games δείχνει στο id του genres
ALTER TABLE games
ADD CONSTRAINT fk_games_genre FOREIGN KEY (genre_id) ____ genres (id);

-- Ερώτημα 4 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Το ίδιο παιχνίδι με genre_id 99, που δεν υπάρχει στον genres
INSERT INTO games (title, genre, release_year, price, added_on, genre_id)
VALUES ('Παιχνίδι Α', 'Παζλ', 2026, 2.99, '2026-10-30', 99);

-- Ερώτημα 5: η ΣΩΣΤΗ εισαγωγή, με είδος που υπάρχει (το 3 είναι το «Παζλ»)
INSERT INTO games (title, genre, release_year, price, added_on, genre_id)
VALUES ('Παιχνίδι Β', 'Παζλ', 2026, 2.99, '2026-10-30', ____);

-- Ερώτημα 6 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Προσπάθεια να σβήσεις ένα είδος που το χρησιμοποιούν παιχνίδια
DELETE FROM genres
WHERE id = 3;

-- Ερώτημα 7: ένα είδος που δεν το χρησιμοποιεί κανένα παιχνίδι σβήνεται κανονικά. Πρόσθεσε ένα και σβήσ' το
INSERT INTO genres (name) VALUES ('Δοκιμή');

DELETE FROM genres
WHERE name = '____';

-- Ερώτημα 8 (έτοιμο): μετονόμασε το είδος 3: ΜΙΑ γραμμή αλλάζει, όσα παιχνίδια κι αν έχει
UPDATE genres
SET name = 'Γρίφοι'
WHERE id = 3;

-- Ερώτημα 9 (έτοιμο): η σχέση με το genre_id δεν επηρεάστηκε, αλλά το κείμενο genre των παιχνιδιών ΔΕΝ άλλαξε.
-- Κοίτα τι γράφει κάθε στήλη
SELECT id, title, genre, genre_id
FROM games
WHERE genre_id = 3
ORDER BY id
LIMIT 3;

-- Ερώτημα 10 (έτοιμο): επανάφερε το όνομα και καθάρισε το δοκιμαστικό παιχνίδι
UPDATE genres
SET name = 'Παζλ'
WHERE id = 3;

DELETE FROM games
WHERE title = 'Παιχνίδι Β';
