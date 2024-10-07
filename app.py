from flask import Flask, render_template, request, jsonify
import duckdb
from db_setup import setup_database

app = Flask(__name__)

def get_db_connection():
    return duckdb.connect('mydb.db')

# Initialize the database
setup_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-total-sales')
def get_total_sales():
    conn = get_db_connection()
    result = conn.execute("""
        SELECT SUM(p.price * o.quantity) as total 
        FROM "order" o 
        JOIN product p ON o.product_id = p.product_id
    """).fetchone()
    conn.close()
    
    if result and result[0] is not None:
        return f"${result[0]:,.2f}"
    else:
        # Check if tables are empty
        order_count = conn.execute('SELECT COUNT(*) FROM "order"').fetchone()[0]
        product_count = conn.execute('SELECT COUNT(*) FROM product').fetchone()[0]
        
        if order_count == 0:
            return "No sales data available. The order table is empty."
        elif product_count == 0:
            return "No product data available. The product table is empty."
        else:
            return "No sales data available. Please check your data and query."

@app.route('/get-top-customers')
def get_top_customers():
    conn = get_db_connection()
    result = conn.execute("""
        SELECT c.name, SUM(p.price * o.quantity) as total_spent
        FROM customer c
        JOIN "order" o ON c.customer_id = o.customer_id
        JOIN product p ON o.product_id = p.product_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_spent DESC
        LIMIT 3
    """).fetchall()
    conn.close()
    return render_template('top_customers.html', customers=result)

@app.route('/get-recent-sales')
def get_recent_sales():
    conn = get_db_connection()
    result = conn.execute("""
        SELECT p.name, o.quantity, p.price, o.order_date
        FROM "order" o
        JOIN product p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
        LIMIT 3
    """).fetchall()
    conn.close()
    return render_template('recent_sales.html', sales=result)

@app.route('/add-data', methods=['POST'])
def add_data():
    data_type = request.form.get('data_type')
    conn = get_db_connection()
    
    try:
        if data_type == 'customer':
            name = request.form.get('name')
            email = request.form.get('email')
            result = conn.execute("SELECT COALESCE(MAX(customer_id), 0) + 1 FROM customer").fetchone()
            new_id = result[0]
            conn.execute("INSERT INTO customer (customer_id, name, email) VALUES (?, ?, ?)", 
                         (new_id, name, email))
            message = f"Customer added successfully with ID: {new_id}"
        elif data_type == 'product':
            name = request.form.get('name')
            price = float(request.form.get('price'))
            result = conn.execute("SELECT COALESCE(MAX(product_id), 0) + 1 FROM product").fetchone()
            new_id = result[0]
            conn.execute("INSERT INTO product (product_id, name, price) VALUES (?, ?, ?)", 
                         (new_id, name, price))
            message = f"Product added successfully with ID: {new_id}"
        elif data_type == 'order':
            customer_id = int(request.form.get('customer_id'))
            product_id = int(request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))
            order_date = request.form.get('order_date')
            result = conn.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM \"order\"").fetchone()
            new_id = result[0]
            conn.execute('INSERT INTO "order" (order_id, customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?, ?)', 
                         (new_id, customer_id, product_id, quantity, order_date))
            message = f"Order added successfully with ID: {new_id}"
        else:
            message = "Invalid data type"
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        message = f"Error: {str(e)}"
    finally:
        conn.close()
    
    return jsonify({"message": message})

@app.route('/get-form-fields')
def get_form_fields():
    data_type = request.args.get('data_type')
    if data_type == 'customer':
        return render_template('customer_form.html')
    elif data_type == 'product':
        return render_template('product_form.html')
    elif data_type == 'order':
        return render_template('order_form.html')
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)