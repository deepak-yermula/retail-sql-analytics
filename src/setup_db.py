"""Create a reproducible, synthetic SQLite retail database."""
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / 'retail.db'
SCHEMA = """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    country TEXT NOT NULL
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    product_name TEXT NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TEXT NOT NULL,
    order_status TEXT NOT NULL CHECK (order_status IN ('completed', 'cancelled'))
);
CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    PRIMARY KEY (order_id, product_id)
);
"""

def create_db(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
        conn.executemany('INSERT INTO customers VALUES (?, ?, ?)', [
            (1, 'Alex Kim', 'Canada'), (2, 'Taylor Lee', 'Canada'),
            (3, 'Jordan Chen', 'USA'), (4, 'Morgan Patel', 'USA')])
        conn.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', [
            (1, 'Electronics', 'Laptop', 50000),
            (2, 'Accessories', 'Mouse', 2500),
            (3, 'Accessories', 'Keyboard', 7500),
            (4, 'Electronics', 'Monitor', 12500)])
        conn.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', [
            (1001, 1, '2026-01-03', 'completed'),
            (1002, 2, '2026-01-17', 'completed'),
            (1003, 3, '2026-02-02', 'completed'),
            (1004, 4, '2026-02-09', 'cancelled')])
        conn.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?)', [
            (1001, 1, 1, 50000),
            (1001, 2, 1, 2500),
            (1002, 3, 1, 7500),
            (1003, 4, 1, 12500),
            (1004, 1, 1, 50000)])
    return db_path

if __name__ == '__main__':
    print(f'Synthetic database created at {create_db()}')
