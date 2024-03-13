import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash

def create_user_table():
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT
        )
    ''')
    connection.commit()
    connection.close()

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def add_user(username, password, email, name):
    if not validate_email(email):
        raise ValueError("Invalid email format")

    hashed_password = generate_password_hash(password)
    
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, email, name)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, email, name))
    connection.commit()
    connection.close()

def login(username, password):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    stored_password = cursor.fetchone()
    connection.close()
    
    if stored_password and check_password_hash(stored_password[0], password):
        return True
    else:
        return False

# CRUD operations for employees
def create_employee_table():
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT UNIQUE
        )
    ''')
    connection.commit()
    connection.close()

def add_employee(name, department, position, email):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO employees (name, department, position, email)
        VALUES (?, ?, ?, ?)
    ''', (name, department, position, email))
    connection.commit()
    connection.close()

def get_all_employees():
    print("Fetching all employees from the database...")  # Debug print
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, department, position, email FROM employees')
    employees = cursor.fetchall()
    connection.close()
    print(f"Employees fetched: {employees}")  # Debug print to see the data
    return employees


def update_employee(employee_id, name, department, position, email):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE employees
        SET name = ?, department = ?, position = ?, email = ?
        WHERE id = ?
    ''', (name, department, position, email, employee_id))
    connection.commit()
    connection.close()

def view_employees():
    global employee_listbox  # Use the global listbox variable
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, department, position, email FROM employees')
    employees = cursor.fetchall()
    connection.close()

    # Clear the existing items in the listbox
    employee_listbox.delete(0, 'end')

    # Insert the retrieved employee data into the listbox
    for employee in employees:
        employee_listbox.insert('end', f"ID: {employee[0]}, Name: {employee[1]}, Department: {employee[2]}, Position: {employee[3]}, Email: {employee[4]}")



def delete_employee(employee_id):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
    connection.commit()
    connection.close()
def add_employee_to_database(name, department, position, email):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO employees (name, department, position, email)
            VALUES (?, ?, ?, ?)
        ''', (name, department, position, email))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in insert operation: {e}")
    finally:
        connection.close()
