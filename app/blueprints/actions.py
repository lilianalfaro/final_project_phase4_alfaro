from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

actions = Blueprint('actions', __name__)

@actions.route('/actions', methods=['GET', 'POST'])
def list_and_create_actions():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new action
    if request.method == 'POST':
        safety_observation_id = request.form['safety_observation_id']
        employee_id = request.form['employee_id']
        action_date = request.form['action_date']
        action_description = request.form['action_description']
        action_status = request.form['action_status']

        # Insert the new action into the database
        cursor.execute(
            '''
            INSERT INTO actions (safety_observation_id, employee_id, action_date, action_description, action_status)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (safety_observation_id, employee_id, action_date, action_description, action_status)
        )
        db.commit()

        flash('New action added successfully!', 'success')
        return redirect(url_for('actions.list_and_create_actions'))

    # Fetch all actions
    cursor.execute('SELECT * FROM actions')
    all_actions = cursor.fetchall()

    # Fetch related data for dropdowns
    cursor.execute('SELECT safety_observation_id, description FROM safety_observations')
    safety_observations = cursor.fetchall()

    cursor.execute('SELECT employee_id, first_name, last_name FROM employees')
    employees = cursor.fetchall()

    return render_template('actions.html', actions=all_actions, safety_observations=safety_observations, employees=employees)

@actions.route('/update_action/<int:action_id>', methods=['GET', 'POST'])
def update_action(action_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        safety_observation_id = request.form['safety_observation_id']
        employee_id = request.form['employee_id']
        action_date = request.form['action_date']
        action_description = request.form['action_description']
        action_status = request.form['action_status']

        cursor.execute(
            '''
            UPDATE actions
            SET safety_observation_id = %s, employee_id = %s, action_date = %s,
                action_description = %s, action_status = %s
            WHERE action_id = %s
            ''',
            (safety_observation_id, employee_id, action_date, action_description, action_status, action_id)
        )
        db.commit()

        flash('Action updated successfully!', 'success')
        return redirect(url_for('actions.list_and_create_actions'))

    # Fetch current action data
    cursor.execute('SELECT * FROM actions WHERE action_id = %s', (action_id,))
    current_action = cursor.fetchone()

    # Fetch related data for dropdowns
    cursor.execute('SELECT safety_observation_id, description FROM safety_observations')
    safety_observations = cursor.fetchall()

    cursor.execute('SELECT employee_id, first_name, last_name FROM employees')
    employees = cursor.fetchall()

    return render_template('update_action.html', action=current_action, safety_observations=safety_observations, employees=employees)

@actions.route('/delete_action/<int:action_id>', methods=['POST'])
def delete_action(action_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM actions WHERE action_id = %s', (action_id,))
    db.commit()

    flash('Action deleted successfully!', 'danger')
    return redirect(url_for('actions.list_and_create_actions'))
