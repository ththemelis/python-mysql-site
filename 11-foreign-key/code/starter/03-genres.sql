-- Στάδιο 2 — Ο πίνακας genres και η στήλη genre_id.
--
-- Πριν αρχίσεις: ο games πρέπει να έχει 30 γραμμές (01-start-state.sql) και να μην έχει ακόμη στήλη genre_id.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--      (Το ερώτημα 4 είναι ομάδα εντολών: τρέξ' το όλο μαζί.)
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει.

-- Ερώτημα 1: ο νέος πίνακας για τα είδη. Κάθε είδος γράφεται ΜΙΑ φορά και παίρνει δικό του id
CREATE TABLE genres (
  id    INT          NOT NULL ____,
  name  VARCHAR(30)  NOT NULL,
  PRIMARY KEY (id),
  ____ (name)
);

-- Ερώτημα 2 (έτοιμο): τα δέκα είδη, με αυτή τη σειρά (το πρώτο παίρνει id 1, το δεύτερο id 2, κ.ο.κ.)
INSERT INTO genres (name) VALUES
  ('Arcade'),
  ('Αγωνιστικό'),
  ('Παζλ'),
  ('Ρόλων'),
  ('Αθλητικό'),
  ('Πλατφόρμας'),
  ('Στρατηγικής'),
  ('Προσομοίωση'),
  ('Περιπέτεια'),
  ('Δράσης');

SELECT id, name
FROM genres
ORDER BY id;

-- Ερώτημα 3: στον games, νέα στήλη που θα δείχνει σε ποιο είδος ανήκει το παιχνίδι: το id του είδους
-- (ίδιος τύπος με το id του genres, και προς το παρόν επιτρέπει NULL)
ALTER TABLE games ADD genre_id ____ NULL;

-- Ερώτημα 4 (έτοιμο): συμπλήρωσε τη genre_id, ένα UPDATE για κάθε είδος (στο Μάθημα 12 θα δεις πώς γίνεται με μία εντολή)
UPDATE games SET genre_id = 1 WHERE genre = 'Arcade';
UPDATE games SET genre_id = 2 WHERE genre = 'Αγωνιστικό';
UPDATE games SET genre_id = 3 WHERE genre = 'Παζλ';
UPDATE games SET genre_id = 4 WHERE genre = 'Ρόλων';
UPDATE games SET genre_id = 5 WHERE genre = 'Αθλητικό';
UPDATE games SET genre_id = 6 WHERE genre = 'Πλατφόρμας';
UPDATE games SET genre_id = 7 WHERE genre = 'Στρατηγικής';
UPDATE games SET genre_id = 8 WHERE genre = 'Προσομοίωση';
UPDATE games SET genre_id = 9 WHERE genre = 'Περιπέτεια';
UPDATE games SET genre_id = 10 WHERE genre = 'Δράσης';

-- Ερώτημα 5: έλεγχος. Ποια παιχνίδια ΔΕΝ πήραν genre_id; (πρέπει να είναι 0)
SELECT COUNT(*)
FROM games
WHERE genre_id IS ____;

-- Ερώτημα 6 (έτοιμο): δες την αντιστοιχία: το είδος ως κείμενο και ως id, δίπλα-δίπλα
SELECT id, title, genre, genre_id
FROM games
ORDER BY id
LIMIT 6;

-- Ερώτημα 7: πόσα παιχνίδια έχει κάθε είδος, τώρα με το genre_id; (βλέπεις αριθμούς, όχι ονόματα:
-- τα ονόματα θα τα φέρει το JOIN του Μαθήματος 12)
SELECT genre_id, COUNT(*) AS n
FROM games
GROUP BY ____
ORDER BY n DESC, genre_id;
