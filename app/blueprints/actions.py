from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pymysql.cursors  # If you're using PyMySQL; adjust if using another library

actions = Blueprint('actions', __name__)

@actions.route('/actions', methods=['GET', 'POST'])
def list_and_create_actions():
    db = get_db()
    # Use a dict cursor. If you are using MySQL Connector/Python:
    # cursor = db.cursor(dictionary=True)
    # If PyMySQL:
    cursor = db.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        safety_observation_id = request.form.get('safety_observation_id')
        employee_id = request.form.get('employee_id')
        action_date = request.form.get('action_date')
        action_description = request.form.get('action_description')
        action_status = request.form.get('action_status')

        if not (safety_observation_id and employee_id and action_date and action_description and action_status):
            flash("All fields are required!", "danger")
        else:
            cursor.execute('''
                INSERT INTO actions (safety_observation_id, employee_id, action_date, action_description, action_status)
                VALUES (%s, %s, %s, %s, %s)
            ''', (safety_observation_id, employee_id, action_date, action_description, action_status))
            db.commit()
            flash('Action added successfully!', 'success')
            return redirect(url_for('actions.list_and_create_actions'))

    # Fetch Actions
    cursor.execute('''
        SELECT a.action_id,
               s.description AS observation_description,
               CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
               a.action_date,
               a.action_description,
               a.action_status
        FROM actions a
        LEFT JOIN safety_observations s ON a.safety_observation_id = s.safety_observation_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
        ORDER BY a.action_id DESC
    ''')
    all_actions = cursor.fetchall()

    # Fetch Safety Observations
    cursor.execute('SELECT safety_observation_id, description FROM safety_observations')
    safety_observations = cursor.fetchall()

    # Fetch Employees
    cursor.execute('SELECT employee_id, CONCAT(first_name, " ", last_name) AS full_name FROM employees')
    employees = cursor.fetchall()

    return render_template(
        'actions.html',
        actions=all_actions,
        safety_observations=safety_observations,
        employees=employees
    )

@actions.route('/delete_action/<int:action_id>', methods=['POST'])
def delete_action(action_id):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('DELETE FROM actions WHERE action_id = %s', (action_id,))
    db.commit()
    flash('Action deleted successfully!', 'danger')
    return redirect(url_for('actions.list_and_create_actions'))

@actions.route('/update_action/<int:action_id>', methods=['GET', 'POST'])
def update_action(action_id):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        safety_observation_id = request.form.get('safety_observation_id')
        employee_id = request.form.get('employee_id')
        action_date = request.form.get('action_date')
        action_description = request.form.get('action_description')
        action_status = request.form.get('action_status')

        cursor.execute('''
            UPDATE actions
            SET safety_observation_id = %s,
                employee_id = %s,
                action_date = %s,
                action_description = %s,
                action_status = %s
            WHERE action_id = %s
        ''', (safety_observation_id, employee_id, action_date, action_description, action_status, action_id))
        db.commit()
        flash('Action updated successfully!', 'success')
        return redirect(url_for('actions.list_and_create_actions'))

    # Fetch single action
    cursor.execute('SELECT * FROM actions WHERE action_id = %s', (action_id,))
    action = cursor.fetchone()
    if not action:
        flash('Action not found!', 'danger')
        return redirect(url_for('actions.list_and_create_actions'))

    # Fetch Safety Observations
    cursor.execute('SELECT safety_observation_id, description FROM safety_observations')
    safety_observations = cursor.fetchall()

    # Fetch Employees
    cursor.execute('SELECT employee_id, first_name, last_name FROM employees')
    employees = cursor.fetchall()

    return render_template('update_action.html', action=action, safety_observations=safety_observations, employees=employees)
