from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create books table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        publication_date TEXT
    )
''')
conn.commit()

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.get_json()

        # Extract book details from the JSON data
        title = data['title']
        author = data['author']
        publication_date = data['publication_date']

        # Add a new book to the database
        cursor.execute('INSERT INTO books (title, author, publication_date) VALUES (?, ?, ?)',
                       (title, author, publication_date))
        conn.commit()

        response = {'message': 'Book added successfully'}
        status_code = 201  # Created
    except Exception as e:
        response = {'error': str(e)}
        status_code = 500  # Internal Server Error

    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)
