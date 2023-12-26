from flask import Flask, request, jsonify
import sqlite3

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

@app.route('/get_books', methods=['GET'])
def get_books():
    try:
        # Retrieve all books from the database
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        # Format the books as a list of dictionaries
        books_list = [{'id': book[0], 'title': book[1], 'author': book[2], 'publication_date': book[3]}
                      for book in books]

        response = {'books': books_list}
        status_code = 200  #
