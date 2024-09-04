import pandas as pd
from apyori import apriori as apriori_algorithm
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import csv
from io import StringIO

app = Flask(__name__)
CORS(app)

# Step 1: Load and preprocess the dataset
chunk_size = 5000
chunks = pd.read_csv('transactions.csv', chunksize=chunk_size)
df = pd.concat(chunks, ignore_index=True)

print(df.columns)

# Create the target column based on Price
df['target_column'] = df['Price'].apply(lambda x: 1 if x > 1000 else 0)

# Drop any rows with missing values and apply one-hot encoding
df.dropna(inplace=True)
df = pd.get_dummies(df, drop_first=True)

# Split the data into features (X) and target (y)
X = df.drop('target_column', axis=1)
y = df['target_column']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 2: Train the RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save the trained model
joblib.dump(model, 'trained_model.pkl')
print('Model saved as trained_model.pkl')

# Load the trained model with error handling
try:
    clf = joblib.load('trained_model.pkl')
except FileNotFoundError:
    print("Model file not found. Ensure that the model has been trained and saved.")
    exit(1)
except EOFError:
    print("Model file is empty or corrupted. Re-run the training process to regenerate it.")
    exit(1)
except pickle.UnpicklingError:
    print("Error unpickling the model file. Ensure the file is not corrupted.")
    exit(1)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="market_basket_db"
    )
    return conn

# Apriori algorithm functions
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

# Route for Apriori algorithm
@app.route('/apriori', methods=['POST'])
def apriori_route():
    print("Apriori route hit")  # Debug statement to check if route is hit
    data = request.get_data(as_text=True)  # Get raw data as a string
    csv_reader = csv.reader(StringIO(data))
    
    transactions = []

    for row in csv_reader:
        # In the CSV format, you do not have a header row, so directly append the transaction items
        transactions.append(row)
    
    # Set minimum support and confidence values
    min_support = 0.3
    min_confidence = 0.3
    
    # Apply the Apriori algorithm
    freq_itemsets, itemset_support = apriori(transactions, min_support)
    
    # Generate association rules
    rules = generate_rules(freq_itemsets, itemset_support, min_confidence)
    
    # Create a list to store associated itemsets
    associated_itemsets = []

    # Extract the associated itemsets from the rules
    for rule in rules:
        antecedent = rule['antecedent']
        consequent = rule['consequent']
        associated_itemsets.append({
            'antecedent': antecedent,
            'consequent': consequent,
            'confidence': rule['confidence']
        })
    
    return jsonify({
        'frequent_itemsets': freq_itemsets,
        'rules': rules,
        'associated_itemsets': associated_itemsets
    })


# Route for getting the stock count of all products
@app.route("/api/stock-count", methods=["GET"])
def get_stock_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT product_name, quantity FROM StockDetails")
    stock_count = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(stock_count)

# Route for getting the total number of customers
@app.route("/api/total-customers", methods=["GET"])
def get_total_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS total_customers FROM CustomerDetails")
    total_customers = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({"total_customers": total_customers})

# Route for getting information of all employees
@app.route("/api/employees", methods=["GET"])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, position, department FROM EmployeeDetails")
    employees = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(employees)

# Route for getting daily transactions
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

# Route for getting daily sales
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

# Route for updating the employee table
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
        conn.commit()
        message = "Employee information updated successfully"
    else:
        # Insert new employee information
        query = """
            INSERT INTO EmployeeDetails (id, name, position, department)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (employee_id, name, position, department))
        conn.commit()
        message = "New employee added successfully"

    cursor.close()
    conn.close()

    return jsonify({"message": message})

# Route for predicting using the trained model
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = [data['feature1'], data['feature2'], data['feature3']]  # Adjust based on your features
    prediction = clf.predict([features])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
