-- Στάδιο 4 — Συναλλαγές στο phpMyAdmin: START TRANSACTION, COMMIT, ROLLBACK.
--
-- Τρέχεις αυτό το αρχείο στην καρτέλα SQL της βάσης game_library (ΟΧΙ με Import), ένα ΒΗΜΑ τη φορά. Κάθε βήμα είναι ένα ΜΠΛΟΚ: αντίγραψε
-- ΟΛΟ το μπλοκ (από τη γραμμή «-- Βήμα» ως το κενό πριν από το επόμενο) στο πεδίο SQL και πάτα Go ΜΙΑ φορά. Το phpMyAdmin τρέχει όλες τις
-- εντολές του μπλοκ στην ΙΔΙΑ σύνδεση και δείχνει το αποτέλεσμα της καθεμιάς.
--
-- Πριν από κάθε βήμα ΠΡΟΒΛΕΨΕ τι θα δείξει το κάθε SELECT.
-- Προϋπόθεση: έχεις τρέξει το 02-loans.sql (το Star Dodger, id 1, έχει 1 διαθέσιμο αντίτυπο και υπάρχουν 4 δανεισμοί).

-- Βήμα 1 (έτοιμο): η αρχική κατάσταση. Πόσα αντίτυπα έχει το Star Dodger;
SELECT id, title, copies_available FROM games WHERE id = 1;

-- Βήμα 2: ΔΟΚΙΜΗ με ROLLBACK. Η συναλλαγή αρχίζει, αλλάζει ένα αντίτυπο, το δείχνει, και μετά ΑΚΥΡΩΝΕΤΑΙ.
____ TRANSACTION;
UPDATE games SET copies_available = copies_available - 1 WHERE id = 1;
-- ΜΕΣΑ στη συναλλαγή:
SELECT id, title, copies_available FROM games WHERE id = 1;
____;
-- ΜΕΤΑ το τέλος της:
SELECT id, title, copies_available FROM games WHERE id = 1;

-- Βήμα 3: το ίδιο, αλλά τώρα η συναλλαγή ΟΡΙΣΤΙΚΟΠΟΙΕΙΤΑΙ.
START TRANSACTION;
UPDATE games SET copies_available = copies_available - 1 WHERE id = 1;
____;
SELECT id, title, copies_available FROM games WHERE id = 1;

-- Βήμα 4 (έτοιμο): ΧΩΡΙΣ START TRANSACTION. Το phpMyAdmin δουλεύει με «αυτόματο COMMIT» (autocommit): κάθε εντολή οριστικοποιείται αμέσως.
-- Πρόβλεψη: τι θα δείξει το SELECT; Θα «γυρίσει πίσω» το ROLLBACK την αλλαγή;
UPDATE games SET copies_available = 1 WHERE id = 1;
ROLLBACK;
SELECT id, title, copies_available FROM games WHERE id = 1;

-- Βήμα 5 (έτοιμο): ένα ΣΦΑΛΜΑ στη μέση. Το Pixel Racer (id 2) δεν έχει διαθέσιμα αντίτυπα, άρα το δεύτερο UPDATE θα αποτύχει (CHECK).
-- Πρόβλεψη: θα μείνει ο νέος δανεισμός στον loans;
START TRANSACTION;
INSERT INTO loans (game_id, member_id) VALUES (2, 4);
UPDATE games SET copies_available = copies_available - 1 WHERE id = 2;
COMMIT;

-- Βήμα 6 (έτοιμο): πόσοι δανεισμοί υπάρχουν τώρα;
SELECT COUNT(*) AS loans_n FROM loans;
