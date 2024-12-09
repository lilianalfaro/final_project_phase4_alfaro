from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

employees = Blueprint('employees', __name__)

@employees.route('/employees', methods=['GET', 'POST'])
def list_and_create_employees():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new employee
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']
        date_hired = request.form['date_hired']

        # Insert the new employee into the database
        cursor.execute(
            '''
            INSERT INTO employees (first_name, last_name, email, role, date_hired)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (first_name, last_name, email, role, date_hired)
        )
        db.commit()

        flash('New employee added successfully!', 'success')
        return redirect(url_for('employees.list_and_create_employees'))

    # Fetch all employees in dictionary format
    cursor.execute('SELECT * FROM employees')
    all_employees = cursor.fetchall()
    return render_template('employees.html', employees=all_employees)

@employees.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']
        date_hired = request.form['date_hired']

        cursor.execute(
            '''
            UPDATE employees
            SET first_name = %s, last_name = %s, email = %s, role = %s, date_hired = %s
            WHERE employee_id = %s
            ''',
            (first_name, last_name, email, role, date_hired, employee_id)
        )
        db.commit()

        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employees.list_and_create_employees'))

    # Fetch employee data to prepopulate form
    cursor.execute('SELECT * FROM employees WHERE employee_id = %s', (employee_id,))
    current_employee = cursor.fetchone()
    return render_template('update_employee.html', employee=current_employee)

@employees.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM employees WHERE employee_id = %s', (employee_id,))
    db.commit()

    flash('Employee deleted successfully!', 'danger')
    return redirect(url_for('employees.list_and_create_employees'))
