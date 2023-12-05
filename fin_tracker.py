import sqlite3 as sql
import matplotlib.pyplot as plt
import os
from datetime import datetime


name_database = 'finances.db'

if not os.path.exists(name_database):
    connection = sql.connect(name_database)
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
    connection = sql.connect(name_database)
    cursor = connection.cursor()


def add_transactions():
    date_str = input('Введите дату транзакции (гггг-мм-дд): ')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print('Неверный формат даты. Используйте корректные гггг-мм-дд')
        return
    
    amount_str = float(input('Введите сумму транзакции: '))
    try:
        amount = float(amount_str)
    except ValueError:
        print('Неверный формат суммы.')
        return
    
    category = input('Введите категорию транзакции: ')
    
    transaction_type = input('Введте тип транзакции (доход/расход): 1/2?')
    
    if transaction_type == '1':
        transaction_type = 'доход'
    
    if transaction_type == '2':
        transaction_type = 'расход'

    if transaction_type not in ('доход', 'расход', '1', '2'):
        print('Неверный тип транзакции. Используйте доход/расход.')
        return

    connection = sql.connect('finances.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transactions (date, amount, category, type) VALUES (?, ?, ?, ?)", (date, amount, category, transaction_type))
    connection.commit()
    connection.close()

question_add = print('Хотите ли вы добавить новую транзакцию? Y/N?')
add_answer = input()
if add_answer == 'Y' or add_answer == 'y':
    add_transactions()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()
elif add_answer == 'N' or add_answer == 'n':
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
        os.remove(name_database)
        print('База данных удалена.')
    else: print('Удаление отменено.')


def display_database():
    connection = sql.connect(name_database)
    cursor = connection.cursor()
    
    # Выполняем SQL-запрос для выборки всех данных из таблицы
    cursor.execute("SELECT * FROM transactions")
    
    # Получаем все строки данных
    rows = cursor.fetchall()
    
    if not rows:
        print("База данных пуста.")
    else:
        for row in rows:
            print(row)
    
    connection.close()

#пока не работает delete_transaction
def delete_transaction(transaction_id):
    connection = sql.connect('finances.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    transaction = cursor.fetchone()

    try:
        transaction_id = int(transaction_id)
    except ValueError:
        print("Неверный формат ID. Введите целое число.")

    if transaction is None:
        print(f"Транзакция с ID {transaction_id} не найдена.")
    else:
        confirmation = input(f"Вы уверены, что хотите удалить транзакцию с ID {transaction_id}? Y/N? ")
        if confirmation == 'Y':
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

            cursor.execute("SELECT id FROM transactions")
            remaining_transaction_ids = [row[0] for row in cursor.fetchall()]

            for new_id, old_id in enumerate(remaining_transaction_ids, start=1):
                cursor.execute("UPDATE transactions SET id = ? WHERE id = ?", (new_id, old_id))

            connection.commit()
            print(f"Транзакция с ID {transaction_id} удалена.")

            display_database()

        else:
            print('Удаление отменено')
    
    connection.close()

#delete_transaction(transaction_id = int(input("Введите id транзакции которую хотите удалить: ")))

#delete_database()

def display_data_visualisation():
    connection = sql.connect('finances.db')
    cursor = connection.cursor()

    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='расход' GROUP BY category")
    data = cursor.fetchall()

    if data:
        categories, amounts = zip(*data)

        plt.bar(categories, amounts, color='blue')
        plt.xlabel('Категории')
        plt.ylabel('Сумма')
        plt.title('Распределение расходов по категориям')
        plt.show()
    
    else: print("Нет данных для визуализации")

    connection.close()

display_data_visualisation()
