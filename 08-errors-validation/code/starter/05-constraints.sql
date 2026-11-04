-- Στάδιο 4 — Οι περιορισμοί της βάσης: UNIQUE, DEFAULT, NULL και CHECK.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import), ώστε ο games να έχει 14 γραμμές.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε αν η εντολή θα πετύχει ή θα δώσει σφάλμα, και ποιο (#αριθμός).
--   4. Οι εντολές με σημείωση «ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ» το δίνουν επίτηδες: δεν είναι δικό σου λάθος.

-- Ερώτημα 1 (έτοιμο): η δομή του πίνακα πριν από τις αλλαγές
DESCRIBE games;

-- Ερώτημα 2: ο τίτλος ενός παιχνιδιού πρέπει να είναι μοναδικός
ALTER TABLE games ADD ____ (title);

-- Ερώτημα 3: ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Ο τίτλος «Mini Golf» υπάρχει ήδη
INSERT INTO games (title, genre, release_year, price)
VALUES ('Mini Golf', 'Αθλητικό', 2024, 3.49);

-- Ερώτημα 4: ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Ο τίτλος δεν επιτρέπεται να είναι «τίποτα» (NULL)
INSERT INTO games (title, genre, release_year, price)
VALUES (____, 'Παζλ', 2024, 1.99);

-- Ερώτημα 5: αν δεν δοθεί είδος, να μπαίνει «Άλλο»
ALTER TABLE games MODIFY genre VARCHAR(30) NOT NULL ____ 'Άλλο';

-- Ερώτημα 6 (έτοιμο): προσθήκη χωρίς είδος και έλεγχος του αποτελέσματος
INSERT INTO games (title, release_year, price)
VALUES ('Quiz Master', 2024, 2.49);

SELECT id, title, genre
FROM games
WHERE title = 'Quiz Master';

-- Ερώτημα 7 (έτοιμο): νέα στήλη που ΕΠΙΤΡΕΠΕΙ NULL (όχι κάθε παιχνίδι έχει περιγραφή)
ALTER TABLE games ADD description VARCHAR(200) NULL;

-- Ερώτημα 8: ποια παιχνίδια ΔΕΝ έχουν περιγραφή; Το NULL ελέγχεται με IS, όχι με =
SELECT id, title
FROM games
WHERE description ____ NULL;

-- Ερώτημα 9: τι γίνεται αν γράψεις «= NULL»; Πρόβλεψε πρώτα πόσες γραμμές θα βγουν
SELECT id, title
FROM games
WHERE description = NULL;

-- Ερώτημα 10 (έτοιμο): δώσε περιγραφή σε ένα παιχνίδι
UPDATE games
SET description = 'Αγώνες με καρτ σε δέκα πίστες'
WHERE id = 9;

-- Ερώτημα 11: ποια παιχνίδια ΕΧΟΥΝ περιγραφή;
SELECT id, title, description
FROM games
WHERE description IS ____ NULL;

-- Ερώτημα 12: έλεγχος τιμών. Η τιμή πρέπει να είναι μεγαλύτερη από 0
ALTER TABLE games ADD CONSTRAINT chk_price ____ (price > 0);

-- Ερώτημα 13: ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Τιμή 0
INSERT INTO games (title, genre, release_year, price)
VALUES ('Δωρεάν παιχνίδι', 'Παζλ', 2024, 0);

-- Ερώτημα 14 (έτοιμο): έλεγχος και για τη χρονιά
ALTER TABLE games ADD CONSTRAINT chk_year CHECK (release_year BETWEEN 1970 AND 2100);

-- Ερώτημα 15: ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Θυμάσαι ότι στο Μάθημα 5 το «abc» στη χρονιά αποθηκευόταν ως 0;
INSERT INTO games (title, genre, release_year, price)
VALUES ('Παιχνίδι χωρίς χρονιά', 'Παζλ', 'abc', 1.99);
