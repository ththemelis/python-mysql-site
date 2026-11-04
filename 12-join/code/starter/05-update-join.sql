-- Στάδιο 4 — JOIN και UPDATE: μία εντολή αντί για πολλές.
--
-- Πριν αρχίσεις: η βάση πρέπει να είναι όπως την άφησε το 01-start-state.sql. Σε αυτό το στάδιο αλλάζεις δεδομένα,
-- αλλά στο τέλος τα επαναφέρεις.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα.

-- Ερώτημα 1 (έτοιμο): συμφωνεί η στήλη genre (κείμενο) με το όνομα του είδους που δείχνει η genre_id;
-- (Το <> σημαίνει «διαφορετικό από».) Δεν πρέπει να βγει καμία γραμμή
SELECT g.id, g.title, g.genre, ge.name
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id
WHERE g.genre <> ge.name;

-- Ερώτημα 2 (έτοιμο): μετονόμασε το είδος 3, όπως στο Μάθημα 11
UPDATE genres
SET name = 'Γρίφοι'
WHERE id = 3;

-- Ερώτημα 3: ξανατρέξε τον έλεγχο. Βρες τα παιχνίδια όπου το κείμενο genre διαφέρει από το όνομα του είδους
SELECT g.id, g.title, g.genre, ge.name
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id
WHERE g.genre ____ ge.name;

-- Ερώτημα 4: διόρθωσε το κείμενο genre ΜΕ ΜΙΑ ΕΝΤΟΛΗ: αντίγραψε το όνομα του είδους στη στήλη genre κάθε παιχνιδιού
UPDATE games AS g
JOIN genres AS ge ON g.genre_id = ge.id
SET g.genre = ge.____;

-- Ερώτημα 5 (έτοιμο): ο έλεγχος ξανά: τώρα δεν πρέπει να βγει καμία γραμμή
SELECT g.id, g.title, g.genre, ge.name
FROM games AS g
JOIN genres AS ge ON g.genre_id = ge.id
WHERE g.genre <> ge.name;

-- Ερώτημα 6 (έτοιμο): επανάφερε το όνομα του είδους και συγχρόνισε ξανά το κείμενο
UPDATE genres
SET name = 'Παζλ'
WHERE id = 3;

UPDATE games AS g
JOIN genres AS ge ON g.genre_id = ge.id
SET g.genre = ge.name;

-- Ερώτημα 7 (έτοιμο): θυμάσαι τα δέκα UPDATE του Μαθήματος 11; Αυτή η ΜΙΑ εντολή κάνει την ίδια δουλειά: γεμίζει τη
-- genre_id από το κείμενο genre. Εδώ όλα έχουν ήδη σωστή τιμή, οπότε δεν αλλάζει τίποτα («0 rows affected»)
UPDATE games AS g
JOIN genres AS ge ON g.genre = ge.name
SET g.genre_id = ge.id;
