-- Οι πέντε ερωτήσεις της βάσης «pizzeria»: το ΠΑΡΑΔΕΙΓΜΑ του Μαθήματος 19 (δεν είναι η δική σου βάση).
--
-- Κάθε ερώτηση είναι ένα ερώτημα SQL. Τρέξε τα ένα-ένα στην καρτέλα SQL της βάσης pizzeria.
-- Οι ερωτήσεις καλύπτουν διαφορετικά εργαλεία: φίλτρο, JOIN πολλών πινάκων, ομάδες, LEFT JOIN και ταξινόμηση με όριο.

USE pizzeria;

-- Ερώτηση 1: Ποια προϊόντα κοστίζουν λιγότερο από 8 €, με τα φθηνότερα πρώτα;   (WHERE, ORDER BY)
SELECT name, price
FROM products
WHERE price < 8
ORDER BY price, name;

-- Ερώτηση 2: Τι περιέχει η παραγγελία 8 και ποιος πελάτης την έκανε;   (JOIN τεσσάρων πινάκων)
SELECT c.name AS customer, p.name AS product, oi.quantity, oi.quantity * p.price AS line_total
FROM customers AS c
JOIN orders      AS o  ON o.customer_id = c.id
JOIN order_items AS oi ON oi.order_id   = o.id
JOIN products    AS p  ON oi.product_id = p.id
WHERE o.id = 8
ORDER BY p.name;

-- Ερώτηση 3: Πόσα έσοδα έχει φέρει κάθε κατηγορία προϊόντων;   (JOIN, GROUP BY, SUM)
SELECT ca.name AS category, SUM(oi.quantity * p.price) AS revenue
FROM categories  AS ca
JOIN products    AS p  ON p.category_id = ca.id
JOIN order_items AS oi ON oi.product_id = p.id
GROUP BY ca.id, ca.name
ORDER BY revenue DESC;

-- Ερώτηση 4: Ποιοι πελάτες δεν έχουν κάνει καμία παραγγελία;   (LEFT JOIN, IS NULL)
SELECT c.name, c.phone
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
WHERE o.id IS NULL;

-- Ερώτηση 5: Ποια είναι τα τρία πιο δημοφιλή προϊόντα (σύνολο τεμαχίων);   (SUM, ORDER BY, LIMIT)
SELECT p.name, SUM(oi.quantity) AS pieces
FROM products    AS p
JOIN order_items AS oi ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY pieces DESC, p.name
LIMIT 3;
