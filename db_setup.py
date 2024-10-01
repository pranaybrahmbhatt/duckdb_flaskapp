import duckdb


def setup_database():
    conn = duckdb.connect("mydb.db")

    # Drop existing tables if they exist, in the correct order
    conn.execute('DROP TABLE IF EXISTS "order"')
    conn.execute("DROP TABLE IF EXISTS product")
    conn.execute("DROP TABLE IF EXISTS customer")

    # Create tables
    conn.execute(
        """
        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE "order" (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id)
        )
    """
    )

    # Populate tables with sample data
    conn.execute(
        """
        INSERT INTO customer (customer_id, name, email) VALUES
        (1, 'John Doe', 'john@example.com'),
        (2, 'Jane Smith', 'jane@example.com'),
        (3, 'Bob Johnson', 'bob@example.com')
    """
    )

    conn.execute(
        """
        INSERT INTO product (product_id, name, price) VALUES
        (1, 'Widget A', 10.99),
        (2, 'Gadget B', 24.99),
        (3, 'Gizmo C', 15.50)
    """
    )

    conn.execute(
        """
        INSERT INTO "order" (order_id, customer_id, product_id, quantity, order_date) VALUES
        (1, 1, 1, 2, '2024-09-01'),
        (2, 1, 2, 1, '2024-09-02'),
        (3, 2, 3, 3, '2024-09-03'),
        (4, 3, 1, 1, '2024-09-04'),
        (5, 2, 2, 2, '2024-09-05')
    """
    )

    conn.close()


if __name__ == "__main__":
    setup_database()
