import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('accounting.db')
cursor = conn.cursor()

# Create transactions table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

def add_transaction(description, amount):
    # Add a new transaction to the database
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO transactions (date, description, amount) VALUES (?, ?, ?)', (date, description, amount))
    conn.commit()
    print('Transaction added successfully.')

def view_ledger():
    # View all transactions in the ledger
    cursor.execute('SELECT * FROM transactions ORDER BY date')
    rows = cursor.fetchall()

    if not rows:
        print('No transactions found.')
    else:
        print('ID | Date                | Description         | Amount')
        print('-' * 50)
        for row in rows:
            print(f'{row[0]:2d} | {row[1]:19} | {row[2]:19} | {row[3]:.2f}')

def calculate_balance():
    # Calculate the current balance
    cursor.execute('SELECT SUM(amount) FROM transactions')
    balance = cursor.fetchone()[0]
    return balance if balance else 0.0

# Simple command-line interface
while True:
    print('\n1. Add Transaction')
    print('2. View Ledger')
    print('3. Calculate Balance')
    print('4. Exit')

    choice = input('Select an option (1-4): ')

    if choice == '1':
        description = input('Enter transaction description: ')
        amount = float(input('Enter transaction amount: '))
        add_transaction(description, amount)
    elif choice == '2':
        view_ledger()
    elif choice == '3':
        balance = calculate_balance()
        print(f'Current Balance: ${balance:.2f}')
    elif choice == '4':
        break
    else:
        print('Invalid option. Please try again.')

# Close the connection when the program exits
conn.close()
