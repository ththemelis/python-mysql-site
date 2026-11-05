-- Στάδιο 3 — JOIN τριών πινάκων: παιχνίδια, πίνακας σύνδεσης και πλατφόρμες.
--
-- Πριν αρχίσεις: έχεις κάνει τα Στάδια 1 και 2 (ο game_platforms έχει 63 γραμμές). Τα ερωτήματα εκτός από το τελευταίο
-- δεν αλλάζουν δεδομένα.
--
-- Πώς το τρέχεις:
--   1. Συμπλήρωσε τα κενά (____) σε έναν επεξεργαστή κειμένου.
--   2. Τρέξε κάθε εντολή ΞΕΧΩΡΙΣΤΑ στην καρτέλα SQL της βάσης game_library, με τη σειρά.
--   3. ΠΡΩΤΑ πρόβλεψε τι θα γίνει: πόσες γραμμές θα έχει το αποτέλεσμα, ή αν θα δώσει σφάλμα και ποιο.

-- Ερώτημα 1: όλα τα ζευγάρια παιχνίδι–πλατφόρμα, με ΟΝΟΜΑΤΑ. Το JOIN περνά από τον πίνακα σύνδεσης: games → game_platforms → platforms
SELECT g.title, p.name AS platform
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id
JOIN platforms AS p ON gp.platform_id = ____.id
ORDER BY g.title, p.name;

-- Ερώτημα 2 (έτοιμο): σε ποιες πλατφόρμες βγαίνει το «Pixel Racer»;
SELECT p.name AS platform
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id
JOIN platforms AS p ON gp.platform_id = p.id
WHERE g.title = 'Pixel Racer'
ORDER BY p.name;

-- Ερώτημα 3: ποια παιχνίδια βγαίνουν στο «Steam Deck»; (τίτλος και τιμή, φθηνότερα πρώτα)
SELECT g.title, g.price
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id
JOIN platforms AS p ON gp.platform_id = p.id
WHERE p.name = '____'
ORDER BY g.price, g.title;

-- Ερώτημα 4 (έτοιμο): η παγίδα του πολλαπλασιασμού. Πόσες γραμμές έχει το αποτέλεσμα, και πόσα διαφορετικά παιχνίδια;
SELECT COUNT(*) AS rows_n, COUNT(DISTINCT g.id) AS games_n
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id
JOIN platforms AS p ON gp.platform_id = p.id;

-- Ερώτημα 5: ποια παιχνίδια ΔΕΝ έχουν καμία πλατφόρμα; (LEFT JOIN και IS NULL, όπως στο Μάθημα 12)
SELECT g.id, g.title
FROM games AS g
LEFT JOIN game_platforms AS gp ON gp.game_id = g.id
WHERE gp.____ IS NULL
ORDER BY g.id;

-- Ερώτημα 6: ποια πλατφόρμα δεν έχει κανένα παιχνίδι; Ο πίνακας που θέλεις να κρατήσεις πρέπει να είναι ΑΡΙΣΤΕΡΑ
SELECT p.name
FROM ____ AS p
LEFT JOIN game_platforms AS gp ON gp.platform_id = p.id
WHERE gp.game_id IS NULL;

-- Ερώτημα 7: πόσα παιχνίδια έχει κάθε πλατφόρμα, ΣΥΜΠΕΡΙΛΑΜΒΑΝΟΜΕΝΗΣ αυτής που δεν έχει κανένα;
SELECT p.name, COUNT(____.game_id) AS games_n
FROM platforms AS p
LEFT JOIN game_platforms AS gp ON gp.platform_id = p.id
GROUP BY p.id, p.name
ORDER BY games_n DESC, p.name;

-- Ερώτημα 8: ΜΙΑ γραμμή για κάθε παιχνίδι, με όλες τις πλατφόρμες του σε ένα κελί. Η GROUP_CONCAT ενώνει τις τιμές μιας ομάδας σε ένα κείμενο
SELECT g.title, ____(p.name ORDER BY p.name SEPARATOR ', ') AS platforms
FROM games AS g
JOIN game_platforms AS gp ON gp.game_id = g.id
JOIN platforms AS p ON gp.platform_id = p.id
GROUP BY g.id, g.title
ORDER BY g.title
LIMIT 8;

-- Ερώτημα 9 (έτοιμο): ΘΑ ΔΩΣΕΙ ΣΦΑΛΜΑ. Διαγραφή παιχνιδιού που έχει πλατφόρμες
DELETE FROM games
WHERE id = 3;
