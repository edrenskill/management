from tkinter import Tk, Label, Entry, Button, Toplevel, Listbox, messagebox, ttk
from user_management import login, add_user, get_all_employees, delete_employee, view_employees
import sqlite3

def show_landing_page():
    landing_window = Toplevel()
    landing_window.title("Employee Management")

    Button(landing_window, text="Add Employee", command=open_add_employee_form).pack(fill='x')
    Button(landing_window, text="Delete Selected Employee", command=delete_selected_employee).pack(fill='x')
    Button(landing_window, text="View Employees", command=view_employees).pack(fill='x')

    global employee_listbox
    employee_listbox = Listbox(landing_window)
    employee_listbox.pack(fill='both', expand=True)

    # update_employee_listbox()

def update_employee_listbox():
    employee_listbox.delete(0, 'end')  # Clear the existing items in the listbox
    # Fetch all employees from the database
    employees = get_all_employees()
    # Iterate over each employee and insert their information into the listbox
    for employee in employees:
        # Assuming employee is a tuple with fields (id, name, department, position, email)
        # You can format the employee information as desired
        employee_listbox.insert('end', f"ID: {employee[0]}, Name: {employee[1]}, Department: {employee[2]}, Position: {employee[3]}, Email: {employee[4]}")

def open_add_employee_form():
    add_employee_window = Toplevel()
    add_employee_window.title("Add Employee")

    # Add Entry widgets for employee details (name, department, position, email)
    Label(add_employee_window, text="Name:").grid(row=0, column=0)
    name_entry = Entry(add_employee_window)
    name_entry.grid(row=0, column=1)

    Label(add_employee_window, text="Department:").grid(row=1, column=0)
    department_entry = Entry(add_employee_window)
    department_entry.grid(row=1, column=1)

    Label(add_employee_window, text="Position:").grid(row=2, column=0)
    position_entry = Entry(add_employee_window)
    position_entry.grid(row=2, column=1)

    Label(add_employee_window, text="Email:").grid(row=3, column=0)
    email_entry = Entry(add_employee_window)
    email_entry.grid(row=3, column=1)

    # Button to add the employee
    Button(add_employee_window, text="Add", command=lambda: add_employee(
        name_entry.get(),
        department_entry.get(),
        position_entry.get(),
        email_entry.get(),
        add_employee_window
    )).grid(row=4, column=0, columnspan=2)

def add_employee(name, department, position, email, window):
    try:
        # Call the function to add the employee to the database
        add_employee_to_database(name, department, position, email)
        messagebox.showinfo("Success", "Employee added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add employee: {e}")

    # Close the add employee window after adding the employee
    window.destroy()

def add_employee_to_database(name, department, position, email):
    connection = sqlite3.connect('management_system.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO employees (name, department, position, email)
            VALUES (?, ?, ?, ?)
        ''', (name, department, position, email))
        connection.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Failed to add employee: Duplicate email.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add employee: {e}")
    finally:
        connection.close()


def delete_selected_employee():
    selected_index = employee_listbox.curselection()
    if selected_index:
        employee_id = employee_listbox.get(selected_index)[0]  # Get the ID from the selected item
        delete_employee(employee_id)
        update_employee_listbox()
        messagebox.showinfo("Success", "Employee deleted successfully.")
    else:
        messagebox.showwarning("Warning", "Please select an employee to delete.")

def view_employees():
    view_window = Toplevel()
    view_window.title("View Employees")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Department", "Position", "Email", "Action"), show="headings")
    tree.pack(expand=True, fill='both')

    # Define headings
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Fetch employees
    employees = get_all_employees()
    
    for employee in employees:
        # Assuming employee is a tuple (id, name, department, position, email)
        # Append a placeholder for the "View" action
        tree.insert("", 'end', values=(*employee, "View"))

    # Handling click event on the Treeview
    def on_item_clicked(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            employee_id = item["values"][0]  # Assuming the first value is the ID
            open_fingerprint_window(employee_id)
            break  # Assuming only one item is selected at a time

    tree.bind("<Double-1>", on_item_clicked)  # Double click to open fingerprint window


def open_fingerprint_window(employee_id):
    fingerprint_window = Toplevel()
    fingerprint_window.title(f"Fingerprint Operations for Employee ID {employee_id}")
    
    # Add your UI components for fingerprint registration and preview here
    Label(fingerprint_window, text="Fingerprint Registration and Preview").pack()

    # Example of a button, add your actual functionality
    Button(fingerprint_window, text="Register Fingerprint").pack()
    Button(fingerprint_window, text="Preview Fingerprint").pack()

def attempt_login():
    username = username_entry.get()
    password = password_entry.get()
    if login(username, password):
        show_landing_page()
        root.withdraw()  # Hide the login window after successful login
    else:
        messagebox.showerror("Login failed", "Incorrect username or password")

def open_registration_form():
    registration_window = Toplevel(root)
    registration_window.title("Registration Form")

    Label(registration_window, text="Username:").grid(row=0, column=0)
    reg_username_entry = Entry(registration_window)
    reg_username_entry.grid(row=0, column=1)

    Label(registration_window, text="Password:").grid(row=1, column=0)
    reg_password_entry = Entry(registration_window, show="*")
    reg_password_entry.grid(row=1, column=1)

    Label(registration_window, text="Email:").grid(row=2, column=0)
    reg_email_entry = Entry(registration_window)
    reg_email_entry.grid(row=2, column=1)

    Label(registration_window, text="Name:").grid(row=3, column=0)
    reg_name_entry = Entry(registration_window)
    reg_name_entry.grid(row=3, column=1)

    Button(registration_window, text="Register", command=lambda: attempt_registration(
        reg_username_entry.get(),
        reg_password_entry.get(),
        reg_email_entry.get(),
        reg_name_entry.get(),
        registration_window
    )).grid(row=4, column=0, columnspan=2)

def attempt_registration(username, password, email, name, window):
    try:
        add_user(username, password, email, name)
        messagebox.showinfo("Registration successful", "User registered successfully.")
    except ValueError as e:
        messagebox.showerror("Registration failed", str(e))
    window.destroy()

root = Tk()
root.title("Login Form")

Label(root, text="Username:").grid(row=0, column=0)
username_entry = Entry(root)
username_entry.grid(row=0, column=1)

Label(root, text="Password:").grid(row=1, column=0)
password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=1)

Button(root, text="Login", command=attempt_login).grid(row=2, column=0, columnspan=2)
Button(root, text="Register", command=open_registration_form).grid(row=3, column=0, columnspan=2)

root.mainloop()
