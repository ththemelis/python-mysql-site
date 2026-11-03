-- Στάδιο 2 — Προσθήκη πλατφορμών.
--
-- Πρέπει πρώτα να έχεις τρέξει το Στάδιο 1 (να υπάρχει ο πίνακας platforms).
-- Συμπλήρωσε τα κενά (____) και τρέξε όλο το αρχείο στην καρτέλα SQL της βάσης game_library.
--
-- Δεν γράφουμε id: το βάζει η βάση μόνη της (AUTO_INCREMENT).

-- TODO 1: πρόσθεσε μία εγγραφή: PlayStation 5, κατασκευαστής Sony, χρονιά 2020
INSERT INTO platforms (name, maker, release_year)
VALUES ('PlayStation 5', ____, ____);

-- TODO 2: πρόσθεσε με ΜΙΑ εντολή τρεις εγγραφές. Η πρώτη είναι έτοιμη.
--   Nintendo Switch, Nintendo, 2017
--   Steam Deck, Valve, 2022
INSERT INTO platforms (name, maker, release_year)
VALUES
    ('Xbox Series X', 'Microsoft', 2020),
    ____,
    ____;
