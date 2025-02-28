# RESTful API for CSV Data Processing

## Overview

This RESTful API allows users to upload CSV files, retrieve statistical data (mean and median) for numeric columns, and query data based on specific column values.

## Features

- **Upload CSV Files**: Accepts CSV files and stores the data in memory.
- **Retrieve Statistics**: Automatically detects numeric columns and calculates mean and median.
- **Query Data**: Filters rows based on query parameters.
- **API Key Authentication**: Secured endpoints using an API key.

## Requirements

Ensure you have Python installed. Install dependencies using:

```sh
pip install -r requirements.txt
```

### `requirements.txt`

```txt
Flask
python-dotenv
```

## Setting Up the API

1. Clone this repository:
   ```sh
   https://github.com/adarshmadhusoodanan/RESTful-API.git
   cd RESTful-API
   ```
2. Create a `.env` file and add your API key:
   ```sh
   API_KEY=your-secret-api-key
   ```
3. Run the API:
   ```sh
   python app.py
   ```

## API Endpoints

### 1. Upload CSV File

- **Endpoint:** `POST /upload`
- **Headers:** `x-api-key: your-secret-api-key`
- **Body:** Form-data with a CSV file
- **Response:**
  ```json
  {
    "message": "CSV file uploaded successfully",
    "rows_uploaded": 100
  }
  ```

### 2. Get Statistics

- **Endpoint:** `GET /stats`
- **Headers:** `x-api-key: your-secret-api-key`
- **Response:**
  ```json
  {
    "Salary": {
      "mean": 50000.0,
      "median": 45000.0
    },
    "Age": {
      "mean": 30.5,
      "median": 29.0
    }
  }
  ```

### 3. Query Data

- **Endpoint:** `GET /query?column=Department&value=IT`
- **Headers:** `x-api-key: your-secret-api-key`
- **Response:**
  ```json
  [
    { "Name": "John", "Department": "IT", "Salary": "50000" },
    { "Name": "Jane", "Department": "IT", "Salary": "55000" }
  ]
  ```

### 4. Retrieve CSV File Data

- **Endpoint:** `GET /`
- **Response:** Returns the contents of `employees.csv`

## Testing with Postman

1. Set `x-api-key` in **Headers**.
2. Use the above endpoints for testing.

## License

MIT License

