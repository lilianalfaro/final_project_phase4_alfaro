from flask import Blueprint, render_template, request, redirect, url_for, flash
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

        # Insert into database
        cursor.execute(
            'INSERT INTO actions (safety_observation_id, employee_id, action_date, action_description, action_status) '
            'VALUES (%s, %s, %s, %s, %s)',
            (safety_observation_id, employee_id, action_date, action_description, action_status)
        )
        db.commit()
        flash('Action added successfully!', 'success')
        return redirect(url_for('actions.list_and_create_actions'))

    # Fetch actions with JOINs
    query = '''
        SELECT 
            a.action_id,
            s.description AS observation_description,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            a.action_date,
            a.action_description,
            a.action_status
        FROM actions a
        LEFT JOIN safety_observations s ON a.safety_observation_id = s.safety_observation_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
    '''
    cursor.execute(query)
    all_actions = cursor.fetchall()

    # Fetch dropdown data
    cursor.execute('SELECT safety_observation_id, description FROM safety_observations')
    safety_observations = cursor.fetchall()
    cursor.execute('SELECT employee_id, CONCAT(first_name, " ", last_name) AS employee_name FROM employees')
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
    cursor = db.cursor()
    cursor.execute('DELETE FROM actions WHERE action_id = %s', (action_id,))
    db.commit()
    flash('Action deleted successfully!', 'danger')
    return redirect(url_for('actions.list_and_create_actions'))
