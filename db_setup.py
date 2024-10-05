import duckdb

def setup_database():
    conn = duckdb.connect("mydb.db")

    # Drop existing tables if they exist
    conn.execute('DROP TABLE IF EXISTS "order"')
    conn.execute("DROP TABLE IF EXISTS product")
    conn.execute("DROP TABLE IF EXISTS customer")

    # Create tables
    conn.execute("""
        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE "order" (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id)
        )
    """)

    # Add sample data
    conn.execute("""
        INSERT INTO customer (customer_id, name, email) VALUES 
        (1, 'John Doe', 'john@example.com'),
        (2, 'Jane Smith', 'jane@example.com')
    """)

    conn.execute("""
        INSERT INTO product (product_id, name, price) VALUES 
        (1, 'Widget', 10.99),
        (2, 'Gadget', 19.99)
    """)

    conn.execute("""
        INSERT INTO "order" (order_id, customer_id, product_id, quantity, order_date) VALUES 
        (1, 1, 1, 2, '2024-10-04'),
        (2, 2, 2, 1, '2024-10-04')
    """)

    conn.close()
    print("Database setup complete with sample data.")

if __name__ == "__main__":
    setup_database()