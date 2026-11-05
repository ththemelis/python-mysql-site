-- Στάδιο 4 — Ο λογαριασμός της εφαρμογής του project σου.
--
-- Όπως στο Μάθημα 17: η εφαρμογή ΔΕΝ συνδέεται ως root. Παίρνει έναν δικό της λογαριασμό, που μπορεί να διαβάζει και να αλλάζει γραμμές ΜΟΝΟ στη βάση του
-- project σου. Τρέξε το ΩΣ root (στο phpMyAdmin είσαι ήδη root), ένα ερώτημα τη φορά, στην καρτέλα SQL.
--
-- 1. Αντικατέστησε το my_project με το όνομα της βάσης σου. Αν θέλεις, άλλαξε και το όνομα του λογαριασμού (project_app): τότε πρέπει να το
--    αλλάξεις και στο APP_USER του config.py.
-- 2. Συμπλήρωσε τα τρία κενά (____).
-- 3. Ο κωδικός εδώ είναι κωδικός ΜΑΘΗΜΑΤΟΣ. Αντίγραψε το config_local.example.py ως config_local.py και βάλε εκεί τον ίδιο κωδικό (το config_local.py ΔΕΝ ανεβαίνει στο git).

DROP USER IF EXISTS 'project_app'@'localhost';

-- Ο λογαριασμός, ΜΕ κωδικό
CREATE ____ 'project_app'@'localhost' IDENTIFIED BY 'project-pass-2026';

-- Η εφαρμογή διαβάζει και αλλάζει δεδομένα: τέσσερα δικαιώματα, και μόνο στους πίνακες της βάσης σου (ΟΧΙ CREATE, ALTER ή DROP)
GRANT SELECT, INSERT, UPDATE, ____ ON my_project.* TO 'project_app'@'localhost';

-- Τι δικαιώματα έχει τώρα; Πρέπει να δεις δύο γραμμές
SHOW ____ FOR 'project_app'@'localhost';
