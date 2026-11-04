-- Στάδιο 3 — LEFT JOIN: κράτα και τις γραμμές που δεν έχουν ταίρι.
--
-- Πριν αρχίσεις: η βάση πρέπει να είναι όπως την άφησε το 01-start-state.sql. Τα ερωτήματα αυτού του σταδίου δεν
-- αλλάζουν δεδομένα.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα.

-- Ερώτημα 1 (έτοιμο): INNER JOIN παιχνιδιών και κριτικών. Πόσες γραμμές βγαίνουν; Πόσα διαφορετικά παιχνίδια φαίνονται;
SELECT g.title, r.stars
FROM games AS g
JOIN reviews AS r ON r.game_id = g.id
ORDER BY g.title;

-- Ερώτημα 2: το ίδιο με LEFT JOIN: όλα τα παιχνίδια του αριστερού πίνακα, με κριτική ή χωρίς
SELECT g.title, r.stars
FROM games AS g
____ JOIN reviews AS r ON r.game_id = g.id
ORDER BY g.title;

-- Ερώτημα 3: μόνο τα παιχνίδια ΧΩΡΙΣ καμία κριτική (εκεί που το ταίρι από τον reviews είναι NULL)
SELECT g.title, g.price
FROM games AS g
LEFT JOIN reviews AS r ON r.game_id = g.id
WHERE r.id IS ____
ORDER BY g.title;

-- Ερώτημα 4: ποια είδη δεν έχουν κανένα παιχνίδι; Η σειρά των πινάκων μετράει: ο ΑΡΙΣΤΕΡΟΣ πίνακας είναι αυτός που
-- κρατά όλες τις γραμμές του
SELECT ge.name
FROM ____ AS ge
LEFT JOIN games AS g ON g.genre_id = ge.id
WHERE g.id IS NULL;

-- Ερώτημα 5 (έτοιμο): πόσες γραμμές δίνει το INNER JOIN και πόσες το LEFT JOIN, για τα είδη και τα παιχνίδια;
SELECT COUNT(*) AS inner_rows
FROM genres AS ge
JOIN games AS g ON g.genre_id = ge.id;

SELECT COUNT(*) AS left_rows
FROM genres AS ge
LEFT JOIN games AS g ON g.genre_id = ge.id;

-- Ερώτημα 6 (έτοιμο): ΠΑΓΙΔΑ. Θέλεις όλα τα παιχνίδια, με τα αστέρια ΜΟΝΟ όπου είναι 4 ή περισσότερα. Με το φίλτρο στο
-- WHERE, πόσες γραμμές βγαίνουν; Τι έγινε με τα παιχνίδια χωρίς κριτική;
SELECT g.title, r.stars
FROM games AS g
LEFT JOIN reviews AS r ON r.game_id = g.id
WHERE r.stars >= 4
ORDER BY g.title;

-- Ερώτημα 7: το ίδιο φίλτρο, αλλά ως μέρος του όρου ON
SELECT g.title, r.stars
FROM games AS g
LEFT JOIN reviews AS r ON r.game_id = g.id ____ r.stars >= 4
ORDER BY g.title;
