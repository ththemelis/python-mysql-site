-- Στάδιο 4 — Ο πίνακας των μελών για το εργαστήριο SQL injection.
--
-- Φτιάχνει (ή ξαναφτιάχνει, αν υπάρχει ήδη) τον πίνακα members της game_library με 4 μέλη. Οι κωδικοί φυλάσσονται ως hash, όχι ως κείμενο.
-- Δεν χρειάζεται να συμπληρώσεις κάτι. Τον τρέχεις: (α) πριν το Στάδιο 4, και (β) κάθε φορά που ένα πείραμα χαλάσει τον πίνακα
-- (π.χ. το DROP TABLE που θα δοκιμάσεις ως root).
--
-- Πώς το τρέχεις: στο phpMyAdmin επίλεξε τη βάση game_library, καρτέλα Import, διάλεξε αυτό το αρχείο και πάτα Import.
-- Αγγίζει ΜΟΝΟ τον πίνακα members.

USE game_library;

DROP TABLE IF EXISTS members;

CREATE TABLE members (
  id             INT          NOT NULL AUTO_INCREMENT,
  username       VARCHAR(30)  NOT NULL,
  password_hash  CHAR(64)     NOT NULL,
  role           VARCHAR(10)  NOT NULL DEFAULT 'member',
  PRIMARY KEY (id),
  UNIQUE (username)
);

-- Οι κωδικοί ΔΕΝ αποθηκεύονται ως κείμενο: φυλάσσεται μόνο το hash τους, SHA2(κωδικός, 256).
INSERT INTO members (username, password_hash, role) VALUES
  ('maria', SHA2('maria-2026', 256), 'member'),
  ('nikos', SHA2('nikos-2026', 256), 'member'),
  ('eleni', SHA2('eleni-2026', 256), 'member'),
  ('admin', SHA2('admin-secret-2026', 256), 'admin');
