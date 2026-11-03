-- Στάδιο 1 — Αλλάζω δεδομένα με UPDATE.
--
-- Πριν αρχίσεις: τρέξε το 01-start-state.sql (καρτέλα Import), ώστε ο games να έχει 17 γραμμές.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library.
--   3. ΠΡΩΤΑ πρόβλεψε πόσες γραμμές θα αλλάξουν. Μετά την UPDATE το phpMyAdmin γράφει «N rows affected».

-- Ερώτημα 1 (έτοιμο): πρώτα ΔΕΣ ποιες γραμμές θα αλλάξει το ερώτημα 4. Η SELECT δεν αλλάζει τίποτα.
SELECT id, title, genre, price
FROM games
WHERE genre = 'Αγωνιστικό';

-- Ερώτημα 2: το «Moto Rush» (id 16) κοστίζει 124.90 αντί για 12.49, λάθος από τη δοκιμή. Διόρθωσέ το.
UPDATE games
SET price = ____
WHERE id = 16;

-- Ερώτημα 3: και τα τρία «Mini Golf» να κοστίζουν 3.99
UPDATE games
SET price = 3.99
WHERE ____ = 'Mini Golf';

-- Ερώτημα 4: έκπτωση 10% στα αγωνιστικά (η νέα τιμή είναι το 90% της παλιάς)
UPDATE games
SET price = ROUND(price * ____, 2)
WHERE genre = 'Αγωνιστικό';

-- Ερώτημα 5: το «Sky Pirates» γίνεται είδος «Δράσης» με τιμή 8.99 (δύο στήλες με μία εντολή)
UPDATE games
SET genre = 'Δράσης'____ price = 8.99
WHERE title = 'Sky Pirates';

-- Ερώτημα 6 (έτοιμο): έλεγξε το αποτέλεσμα όλων των αλλαγών
SELECT id, title, genre, price
FROM games
WHERE id IN (2, 9, 11, 12, 13, 14, 16)
ORDER BY id;
