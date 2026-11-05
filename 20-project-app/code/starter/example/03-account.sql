-- Ο λογαριασμός της εφαρμογής «pizzeria» (το παράδειγμα του Μαθήματος 20).
--
-- Όπως στα Μαθήματα 17 και 19: η εφαρμογή ΔΕΝ συνδέεται ως root. Παίρνει έναν δικό της λογαριασμό, που μπορεί να διαβάζει και να αλλάζει γραμμές ΜΟΝΟ στη
-- βάση pizzeria (όχι να φτιάχνει ή να σβήνει πίνακες). Τρέξε το ΩΣ root (στο phpMyAdmin είσαι ήδη root), ένα ερώτημα τη φορά.
-- Ο κωδικός είναι κωδικός ΜΑΘΗΜΑΤΟΣ και μπαίνει στο config_local.py, όχι στον κώδικα.

DROP USER IF EXISTS 'pizzeria_app'@'localhost';
CREATE USER 'pizzeria_app'@'localhost' IDENTIFIED BY 'pizza-pass-2026';
GRANT SELECT, INSERT, UPDATE, DELETE ON pizzeria.* TO 'pizzeria_app'@'localhost';
SHOW GRANTS FOR 'pizzeria_app'@'localhost';
