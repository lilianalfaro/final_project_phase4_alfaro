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

    # Fetch actions with optional filters
    filter_status = request.args.get('filter_status', '')
    query = 'SELECT * FROM actions WHERE 1=1'
    params = []
    if filter_status:
        query += ' AND action_status = %s'
        params.append(filter_status)
    cursor.execute(query, params)
    all_actions = cursor.fetchall()

    # Fetch dropdown data
    cursor.execute('SELECT * FROM safety_observations')
    safety_observations = cursor.fetchall()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()

    return render_template(
        'actions.html',
        actions=all_actions,
        safety_observations=safety_observations,
        employees=employees
    )
