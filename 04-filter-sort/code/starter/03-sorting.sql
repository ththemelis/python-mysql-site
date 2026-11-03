-- Στάδιο 3 — Σειρά, όριο και αναζήτηση με μοτίβο: ORDER BY, LIMIT, LIKE.
--
-- Τρέξε κάθε ερώτημα ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, αφού συμπληρώσεις τα κενά (____).
-- ΠΡΩΤΑ πρόβλεψε ποιο παιχνίδι θα βρίσκεται στην πρώτη γραμμή.

-- Ερώτημα 1 (έτοιμο): από το φθηνότερο στο ακριβότερο
SELECT title, price
FROM games
ORDER BY price;

-- Ερώτημα 2: από το ακριβότερο στο φθηνότερο
SELECT title, price
FROM games
ORDER BY price ____;

-- Ερώτημα 3: τα τρία ακριβότερα παιχνίδια
SELECT title, price
FROM games
ORDER BY price DESC
____ 3;

-- Ερώτημα 4: πρώτα κατά είδος και, μέσα σε κάθε είδος, κατά τίτλο
SELECT genre, title
FROM games
ORDER BY ____, ____;

-- Ερώτημα 5: οι τίτλοι που ΑΡΧΙΖΟΥΝ από S
SELECT title
FROM games
WHERE title LIKE ____;

-- Ερώτημα 6: οι τίτλοι που ΠΕΡΙΕΧΟΥΝ τη λέξη «Kart»
SELECT title
FROM games
WHERE title LIKE ____;

-- Ερώτημα 7 (έτοιμο): οι τίτλοι με δεύτερο γράμμα το i (το _ αντιστοιχεί σε ΕΝΑ οποιοδήποτε γράμμα)
SELECT title
FROM games
WHERE title LIKE '_i%';

-- Ερώτημα 8: από τα παιχνίδια που κοστίζουν λιγότερο από 15 €, οι δύο πιο πρόσφατοι τίτλοι
-- (πρώτα η πιο πρόσφατη χρονιά, και σε ισοπαλία κατά τίτλο). Πρόσεξε τη σειρά των φράσεων.
SELECT title, release_year
FROM games
WHERE ____
ORDER BY release_year DESC, title
LIMIT ____;
