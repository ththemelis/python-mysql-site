-- Το σχήμα της βάσης «pizzeria»: το ΠΑΡΑΔΕΙΓΜΑ του Μαθήματος 20 (το ίδιο με του Μαθήματος 19).
--
-- Πέντε πίνακες: categories, products, customers, orders, order_items.
--   * categories 1:N products        (κάθε προϊόν έχει μία κατηγορία)
--   * customers  1:N orders          (κάθε παραγγελία έχει έναν πελάτη)
--   * orders N:N products            (μέσω του πίνακα σύνδεσης order_items, που έχει και τη στήλη quantity)
--
-- Μπορείς να το τρέξεις όσες φορές θέλεις: σβήνει τους πίνακες και τους ξαναφτιάχνει. Δεν αγγίζει τη βάση game_library.
-- Πώς το τρέχεις: στο phpMyAdmin, καρτέλα Import (χωρίς επιλεγμένη βάση), διάλεξε αυτό το αρχείο και πάτα Import.

CREATE DATABASE IF NOT EXISTS pizzeria
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE pizzeria;

-- Καθαρισμός: πρώτα οι πίνακες που ΑΝΑΦΕΡΟΝΤΑΙ σε άλλους (τα «παιδιά»), μετά οι «γονείς»
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;

-- Δημιουργία: πρώτα οι γονείς, μετά τα παιδιά
CREATE TABLE categories (
  id    INT          NOT NULL AUTO_INCREMENT,
  name  VARCHAR(30)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);

CREATE TABLE customers (
  id       INT           NOT NULL AUTO_INCREMENT,
  name     VARCHAR(60)   NOT NULL,
  phone    VARCHAR(15)   NOT NULL,
  address  VARCHAR(100)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (phone)
);

CREATE TABLE products (
  id           INT           NOT NULL AUTO_INCREMENT,
  name         VARCHAR(60)   NOT NULL,
  category_id  INT           NOT NULL,
  price        DECIMAL(5,2)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name),
  CONSTRAINT chk_products_price CHECK (price > 0),
  CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE orders (
  id           INT          NOT NULL AUTO_INCREMENT,
  customer_id  INT          NOT NULL,
  ordered_at   DATETIME     NOT NULL DEFAULT (NOW()),
  status       VARCHAR(10)  NOT NULL DEFAULT 'new',
  PRIMARY KEY (id),
  CONSTRAINT chk_orders_status CHECK (status IN ('new', 'ready', 'delivered')),
  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- Πίνακας σύνδεσης με ΕΞΤΡΑ στήλη: δύο στήλες στο πρωτεύον κλειδί, και η quantity λέει «πόσα τεμάχια»
CREATE TABLE order_items (
  order_id    INT  NOT NULL,
  product_id  INT  NOT NULL,
  quantity    INT  NOT NULL DEFAULT 1,
  PRIMARY KEY (order_id, product_id),
  CONSTRAINT chk_items_quantity CHECK (quantity BETWEEN 1 AND 20),
  CONSTRAINT fk_items_order   FOREIGN KEY (order_id)   REFERENCES orders (id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (id)
);
