#Create a RESTful API with a single endpoint that allows users to upload a CSV file containing data.
#Implement basic validation to check the format and structure of the uploaded CSV file.

from flask import Flask, request, jsonify
import csv
import io
import os
import statistics
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

data_storage = []  # In-memory storage for CSV data rows



# @app.route('/', methods=['GET'])
# def upload():
#     with open('employees.csv', 'r') as f:
#         reader = csv.reader(f)
#         employees = list(reader)
#     return jsonify(employees)

# Retrieve the API key from the environment variable
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("No API_KEY set for Flask application. Please set it in the .env file.")
# print(f"API Key: {API_KEY   }")


#Implement basic authentication (e.g., a simple API key) to secure the endpoints.
#authentication
def authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):             #decorator function used to check the api key
        provided_key = request.headers.get("x-api-key")
        # print(f"Incoming Headers: {request.headers}") 
        if provided_key != API_KEY:
            # print(f"Unauthorized access with API key: {provided_key}")
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# print(f"Loaded API Key from .env: {API_KEY}")  


#file upload

@app.route('/upload', methods=['POST'])
@authentication
def upload_csv():
    #Implement basic validation to check the format and structure of the uploaded CSV file.

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

    #Store the uploaded data in an in-memory structure (e.g., a list or a simple SQLite database).
    # iam using a list to store the data
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None) # Read the CSV file
    csv_reader = csv.DictReader(stream)
    rows = list(csv_reader)
    data_storage.extend(rows)

    # print(data_storage)
    
    return jsonify({"message": "CSV file uploaded successfully", "rows_uploaded": len(rows)}), 200


#Include a simple data processing step, such as calculating summary statistics (e.g., mean, median) for numerical columns.
#Provide a second endpoint to retrieve these statistics.

@app.route('/stats', methods=['GET'])
@authentication
def get_stats():
    if not data_storage:
        return jsonify({"message": "No data available"}), 400

    numeric_columns = {}

    # Identify numerical columns dynamically
    for row in data_storage:
        for key, value in row.items():
            try:
                num_value = float(value)
                if key not in numeric_columns:
                    numeric_columns[key] = []
                numeric_columns[key].append(num_value)
            except ValueError:
                continue  # Ignore non-numeric values

    if not numeric_columns:
        return jsonify({"message": "No numeric data found in the dataset"}), 400

    # Calculate statistics for each numerical column
    stats = {col: {"mean": statistics.mean(values), "median": statistics.median(values)}
             for col, values in numeric_columns.items()}

    return jsonify(stats), 200



# def get_stats():
#     if not data_storage:
#         return jsonify({"message": "No data available"}), 400

#     # Calculate statistics based on the SALARY column
#     # try:
#     #     salaries = [float(row['SALARY']) for row in data_storage if 'SALARY' in row and row['SALARY'].strip()]
#     # except Exception as e:
#     #     return jsonify({"message": "Data error", "error": str(e)}), 400

#     # if not salaries:
#     #     return jsonify({"message": "No numeric data found in 'SALARY' column"}), 400

#     # stats = {
#     #     "mean_salary": statistics.mean(salaries),
#     #     "median_salary": statistics.median(salaries)
#     # }
#     print(stats)
#     return jsonify(stats), 200

#Add a third endpoint to allow users to query the data (e.g., filter by a specific column value).
@app.route('/query', methods=['GET'])
@authentication
def query_data():
    column = request.args.get("column")
    value = request.args.get("value")
    if not column or not value:
        return jsonify({"message": "Provide both 'column' and 'value' as query parameters"}), 400

    filtered = [row for row in data_storage if row.get(column) == value]
    
    print(filtered)
    return jsonify(filtered), 200
    


if __name__ == '__main__':
    app.run(debug=True)