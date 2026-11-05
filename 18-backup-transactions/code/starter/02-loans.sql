-- Αρχή του Κύκλου 2 — Δανεισμός παιχνιδιών: μία νέα στήλη και ένας νέος πίνακας.
--
-- Η βιβλιοθήκη μας δανείζει παιχνίδια στα μέλη (τον πίνακα members τον έφτιαξες στο Μάθημα 17). Κάθε παιχνίδι έχει 2 αντίτυπα.
--   * games.copies_available: πόσα αντίτυπα είναι διαθέσιμα ΤΩΡΑ (δεν μπορεί να γίνει αρνητικό: CHECK)
--   * loans: ένας δανεισμός = ένα μέλος, ένα παιχνίδι, ημερομηνία δανεισμού, ημερομηνία επιστροφής (NULL = δεν επέστρεψε ακόμη)
--
-- Δεν χρειάζεται να συμπληρώσεις κάτι. Πώς το τρέχεις: στο phpMyAdmin επίλεξε τη βάση game_library, καρτέλα Import,
-- διάλεξε αυτό το αρχείο και πάτα Import. Μπορείς να το ξανατρέξεις όσες φορές θέλεις: ξαναφτιάχνει τον πίνακα
-- loans και ξαναβάζει τα αντίτυπα στην αρχική τους κατάσταση.
--
-- ΠΡΟΣΟΧΗ: τρέχει πάνω στη βάση του Μαθήματος 17 (πίνακες games και members). Αν χαλάσει κάτι, τρέξε πρώτα το 01-start-state.sql.

USE game_library;

-- Καθαρισμός (έτσι ξανατρέχει το αρχείο)
DROP TABLE IF EXISTS loans;
ALTER TABLE games DROP CONSTRAINT IF EXISTS chk_copies;
ALTER TABLE games DROP COLUMN IF EXISTS copies_available;

-- Νέα στήλη: όλα τα παιχνίδια ξεκινούν με 2 διαθέσιμα αντίτυπα
ALTER TABLE games ADD COLUMN copies_available INT NOT NULL DEFAULT 2;
ALTER TABLE games ADD CONSTRAINT chk_copies CHECK (copies_available >= 0);

-- Νέος πίνακας: οι δανεισμοί
CREATE TABLE loans (
  id           INT   NOT NULL AUTO_INCREMENT,
  game_id      INT   NOT NULL,
  member_id    INT   NOT NULL,
  loaned_on    DATE  NOT NULL DEFAULT (CURDATE()),
  returned_on  DATE  NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_loans_game   FOREIGN KEY (game_id)   REFERENCES games (id),
  CONSTRAINT fk_loans_member FOREIGN KEY (member_id) REFERENCES members (id)
);

-- Τέσσερις δανεισμοί: οι τρεις είναι ενεργοί (returned_on NULL), ο ένας έχει ήδη επιστραφεί
INSERT INTO loans (game_id, member_id, loaned_on, returned_on) VALUES
  (1, 1, '2026-10-20', NULL),
  (2, 2, '2026-10-22', NULL),
  (2, 3, '2026-10-25', NULL),
  (5, 1, '2026-10-05', '2026-10-12');

-- Τα αντίτυπα που είναι δανεισμένα δεν είναι διαθέσιμα: το Star Dodger (id 1) έχει 1 ελεύθερο, το Pixel Racer (id 2) κανένα
UPDATE games SET copies_available = 1 WHERE id = 1;
UPDATE games SET copies_available = 0 WHERE id = 2;
