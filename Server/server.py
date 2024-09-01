from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import csv
from io import StringIO


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

#Apriori algorithm
def calculate_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count / len(transactions)

def generate_candidates(prev_freq_itemsets, k):
    candidates = []
    len_prev_itemsets = len(prev_freq_itemsets)
    
    for i in range(len_prev_itemsets):
        for j in range(i + 1, len_prev_itemsets):
            candidate = list(set(prev_freq_itemsets[i]).union(set(prev_freq_itemsets[j])))
            candidate.sort()
            if len(candidate) == k and candidate not in candidates:
                candidates.append(candidate)
    
    return candidates

def filter_itemsets(candidates, transactions, min_support):
    freq_itemsets = []
    itemset_support = {}
    
    for candidate in candidates:
        support = calculate_support(candidate, transactions)
        if support >= min_support:
            freq_itemsets.append(candidate)
            itemset_support[tuple(candidate)] = support
            
    return freq_itemsets, itemset_support

def apriori(transactions, min_support):
    items = sorted(set(item for transaction in transactions for item in transaction))
    candidates = [[item] for item in items]
    all_freq_itemsets = []
    itemset_support = {}
    k = 1
    while candidates:
        freq_itemsets, support_data = filter_itemsets(candidates, transactions, min_support)
        all_freq_itemsets.extend(freq_itemsets)
        itemset_support.update(support_data)
        k += 1
        candidates = generate_candidates(freq_itemsets, k)
    
    return all_freq_itemsets, itemset_support

def generate_rules(freq_itemsets, itemset_support, min_confidence):
    rules = []
    for itemset in freq_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                antecedents = itemset[:i]
                consequents = itemset[i:]
                antecedent_support = itemset_support.get(tuple(antecedents), 0)
                confidence = itemset_support[tuple(itemset)] / antecedent_support
                if confidence >= min_confidence:
                    rules.append({
                        'antecedent': antecedents,
                        'consequent': consequents,
                        'confidence': confidence
                    })
    return rules

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apriori', methods=['POST'])
def apriori_route():
    data = request.get_data(as_text=True)  # Get raw CSV data as a string
    csv_reader = csv.reader(StringIO(data))
    
    transactions = []
    
    # Skip header row
    next(csv_reader)
    
    for row in csv_reader:
        transaction_items = row[1:]  # Skip the TransactionID and get the items
        transactions.append(transaction_items)
    
    # For example, let's assume min_support and min_confidence are set to 0.5 and 0.7 respectively
    min_support = 0.5
    min_confidence = 0.7
    
    freq_itemsets, itemset_support = apriori(transactions, min_support)
    rules = generate_rules(freq_itemsets, itemset_support, min_confidence)
    
    return jsonify({
        'frequent_itemsets': freq_itemsets,
        'rules': rules
    })
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

    # Check if the employee already exists
    check_query = "SELECT * FROM EmployeeDetails WHERE id = %s"
    cursor.execute(check_query, (employee_id,))
    result = cursor.fetchone()

    if result:
        # Update the existing employee information
        query = """
            UPDATE EmployeeDetails 
            SET name = %s, position = %s, department = %s 
            WHERE id = %s
        """
        cursor.execute(query, (name, position, department, employee_id))
    else:
        # Insert a new employee record
        query = """
            INSERT INTO EmployeeDetails (id, name, position, department) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (employee_id, name, position, department))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(data)
    return jsonify({"message": "Employee information updated successfully"}), 200



# Start the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
