from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="market_basket_db"
    )
    return conn

# stock count of all products
@app.route("/api/stock-count", methods=["GET"])
def get_stock_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT product_name, quantity FROM StockDetails")
    stock_count = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(stock_count)

# total number of customers
@app.route("/api/total-customers", methods=["GET"])
def get_total_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS total_customers FROM CustomerDetails")
    total_customers = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({"total_customers": total_customers})

# information of all employees
@app.route("/api/employees", methods=["GET"])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, position, department FROM EmployeeDetails")
    employees = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(employees)

# daily transitions
@app.route("/api/daily-transactions", methods=["GET"])
def get_daily_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Updated SQL query to include S.N., Product Name, Price, and Time
    query = """
        SELECT 
            @row_number := @row_number + 1 AS serial_number, 
            product_name,
            id,
            quantity,
            transaction_date
        FROM transitions
    """
    
    cursor.execute(query)
    daily_transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(daily_transactions)

# daily sales
@app.route("/api/daily-sales", methods=["GET"])
def get_daily_sales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            DATE(timestamp) AS date, 
            HOUR(timestamp) AS hour, 
            COUNT(*) AS transaction_count
        FROM transactions 
        WHERE DATE(timestamp) = CURDATE()
        GROUP BY DATE(timestamp), HOUR(timestamp)
        ORDER BY hour
    """
    cursor.execute(query)
    sales = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(sales)


# Update the database 

#Update emplyoee table
@app.route("/api/update-employee", methods=["POST"])
def update_employee():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get data from the frontend
    data = request.json
    employee_id = data.get("id")
    name = data.get("name")
    position = data.get("position")
    department = data.get("department")

    # Update the employee information
    query = """
        UPDATE EmployeeDetails 
        SET name = %s, position = %s, department = %s 
        WHERE id = %s
    """
    cursor.execute(query, (name, position, department, employee_id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Employee information updated successfully"}), 200


# Start the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
