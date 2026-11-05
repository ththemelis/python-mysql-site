-- Στάδιο 1 — Ο πίνακας σύνδεσης game_platforms.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import).
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα και ποιο.

-- Ερώτημα 1 (έτοιμο): οι πλατφόρμες. Ένα παιχνίδι βγαίνει σε ΠΟΛΛΕΣ πλατφόρμες, και μια πλατφόρμα έχει ΠΟΛΛΑ παιχνίδια
SELECT id, name
FROM platforms
ORDER BY id;

-- Ερώτημα 2: ο πίνακας σύνδεσης. Κάθε γραμμή του λέει: «αυτό το παιχνίδι βγαίνει σε αυτή την πλατφόρμα».
-- Το πρωτεύον κλειδί είναι το ΖΕΥΓΑΡΙ (game_id, platform_id), και κάθε στήλη του είναι ξένο κλειδί
CREATE TABLE game_platforms (
  game_id      INT  NOT NULL,
  platform_id  INT  NOT NULL,
  PRIMARY KEY (game_id, ____),
  CONSTRAINT fk_gp_game     FOREIGN KEY (game_id)     REFERENCES games (id),
  CONSTRAINT fk_gp_platform FOREIGN KEY (platform_id) ____ platforms (____)
);

-- Ερώτημα 3: το «Pixel Racer» (id 2) βγαίνει στις πλατφόρμες 1, 2, 3 και 4. Μία εντολή, τέσσερις γραμμές
INSERT INTO game_platforms (game_id, platform_id)
VALUES (2, 1), (2, 2), (2, ____), (2, 4);

-- Ερώτημα 4 (έτοιμο): τι περιέχει ο πίνακας σύνδεσης;
SELECT game_id, platform_id
FROM game_platforms
ORDER BY game_id, platform_id;

-- Ερώτημα 5 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Το ίδιο ζευγάρι δεύτερη φορά
INSERT INTO game_platforms (game_id, platform_id)
VALUES (2, 1);

-- Ερώτημα 6 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Παιχνίδι που δεν υπάρχει
INSERT INTO game_platforms (game_id, platform_id)
VALUES (999, 1);

-- Ερώτημα 7 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Πλατφόρμα που δεν υπάρχει
INSERT INTO game_platforms (game_id, platform_id)
VALUES (2, 99);
