from flask import Flask, render_template
import duckdb

app = Flask(__name__)

def get_db_connection():
    return duckdb.connect('mydb.db')

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Using a CTE and window function to get total sales per customer
    customer_sales = conn.execute("""
        WITH customer_total_sales AS (
            SELECT 
                c.customer_id,
                c.name,
                SUM(o.quantity * p.price) as total_sales,
                ROW_NUMBER() OVER (ORDER BY SUM(o.quantity * p.price) DESC) as sales_rank
            FROM customer c
            JOIN "order" o ON c.customer_id = o.customer_id
            JOIN product p ON o.product_id = p.product_id
            GROUP BY c.customer_id, c.name
        )
        SELECT * FROM customer_total_sales
    """).fetchall()
    
    # Get top selling products
    top_products = conn.execute("""
        SELECT 
            p.name,
            SUM(o.quantity) as total_quantity,
            SUM(o.quantity * p.price) as total_revenue,
            RANK() OVER (ORDER BY SUM(o.quantity * p.price) DESC) as revenue_rank
        FROM product p
        JOIN "order" o ON p.product_id = o.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_revenue DESC
        LIMIT 5
    """).fetchall()
    
    # Get recent orders
    recent_orders = conn.execute("""
        SELECT 
            o.order_id,
            c.name as customer_name,
            p.name as product_name,
            o.quantity,
            o.order_date,
            o.quantity * p.price as total_price
        FROM "order" o
        JOIN customer c ON o.customer_id = c.customer_id
        JOIN product p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
        LIMIT 10
    """).fetchall()
    
    conn.close()
    
    return render_template('index.html', customer_sales=customer_sales, top_products=top_products, recent_orders=recent_orders)

if __name__ == '__main__':
    app.run(debug=True)