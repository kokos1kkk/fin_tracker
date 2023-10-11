import sqlite3 as sql
import os
from datetime import datetime

if not os.path.exists('finances.db'):
    connection = sql.connect('finances.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            date DATE,
            amount MONEY,
            category TEXT,
            type TEXT
        )
    ''')
    connection.close()

else:
    connection = sql.connect('finances.db')
    cursor = connection.cursor()

def add_transactions():
    date_str = input('Введите дату транзакции (гг-мм-дд): ')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print('Неверный формат даты. Используйте гггг-мм-ддю')
        return
    
    amount_str = float(input('Введите сумму транзакции: '))
    try:
        amount = float(amount_str)
    except ValueError:
        print('Неверный формат суммы.')
        return
    
    category = input('Введите категорию транзакции: ')
    
    transaction_type = input('Введте тип транзакции (доход/расход): ')
    
    if transaction_type not in ('доход', 'расход'):
        print('Неверный тип транзакции. Используйте доход/расход.')
        return

    connection = sql.connect('finances.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transactions (date, amount, category, type) VALUES (?, ?, ?, ?)", (date, amount, category, transaction_type))
    connection.commit()
    connection.close()

question_add = print('Хотите ли вы добавить новую транзакцию? Y/N?')
add_answer = input()
if add_answer == 'Y':
    add_transactions()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()
elif add_answer == 'N':
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()

else:
    print ('Error')

def delete_database():
    confirmation = input('Вы уверены что хотите удалить базу данных? Y/N? ')
    if confirmation == 'Y':
        os.remove('finances.db')
        print('База данных удалена.')
    else: print('Удаление отменено.')


#пока не работает delete_transaction
def delete_transaction(id):
    connection = sql.connect('finances.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (id))
    transaction = cursor.fetchone()

    if transaction is None:
        print(f"Транзакция с ID {id} не найдена.")
    else:
        confirmation = input(f"Вы уверены, что хотите удалить транзакцию с ID {id}? Y/N? ")
        if confirmation.lower() == 'Y':
            id = int(input())
            cursor.execute("DELETE FROM transactions WHERE id = ?", (id))
            connection.commit()
            print(f"Транзакция с ID {id} удалена.")
        else: print('Удаление отменено')
    connection.close()





