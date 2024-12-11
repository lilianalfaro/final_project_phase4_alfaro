from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

safety_observations = Blueprint('safety_observations', __name__)

@safety_observations.route('/safety_observations', methods=['GET', 'POST'])
def list_and_create_safety_observations():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new observation
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        commodity_type = request.form['commodity_type']
        operation = request.form['operation']
        category = request.form['category']
        sub_category = request.form['sub_category']
        severity = request.form['severity']
        status = request.form['status']
        description = request.form['description']

        cursor.execute(
            '''
            INSERT INTO safety_observations 
            (date, time, location, commodity_type, operation, category, sub_category, severity, status, description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (date, time, location, commodity_type, operation, category, sub_category, severity, status, description)
        )
        db.commit()
        flash('New observation added successfully!', 'success')
        return redirect(url_for('safety_observations.list_and_create_safety_observations'))

    # Apply filters
    filter_commodity = request.args.get('filter_commodity', '')
    filter_operation = request.args.get('filter_operation', '')
    filter_category = request.args.get('filter_category', '')

    query = 'SELECT * FROM safety_observations WHERE 1=1'
    params = []

    if filter_commodity:
        query += ' AND commodity_type = %s'
        params.append(filter_commodity)
    if filter_operation:
        query += ' AND operation = %s'
        params.append(filter_operation)
    if filter_category:
        query += ' AND category = %s'
        params.append(filter_category)

    cursor.execute(query, params)
    observations = cursor.fetchall()

    return render_template(
        'safety_observations.html',
        observations=observations,
        filter_commodity=filter_commodity,
        filter_operation=filter_operation,
        filter_category=filter_category
    )

@safety_observations.route('/update_safety_observation/<int:observation_id>', methods=['GET', 'POST'])
def update_safety_observation(observation_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        commodity_type = request.form['commodity_type']
        operation = request.form['operation']
        category = request.form['category']
        sub_category = request.form['sub_category']
        description = request.form['description']
        severity = request.form['severity']
        status = request.form['status']

        # Update the safety observation
        cursor.execute(
            '''
            UPDATE safety_observations
            SET date = %s, time = %s, location = %s, commodity_type = %s, operation = %s,
                category = %s, sub_category = %s, description = %s, severity = %s, status = %s
            WHERE safety_observation_id = %s
            ''',
            (date, time, location, commodity_type, operation, category, sub_category, description, severity, status, observation_id)
        )
        db.commit()
        flash('Safety observation updated successfully!', 'success')
        return redirect(url_for('safety_observations.list_and_create_safety_observations'))

    # Fetch current observation data
    cursor.execute('SELECT * FROM safety_observations WHERE safety_observation_id = %s', (observation_id,))
    current_observation = cursor.fetchone()

    return render_template('update_safety_observation.html', observation=current_observation)

@safety_observations.route('/delete_safety_observation/<int:observation_id>', methods=['POST'])
def delete_safety_observation(observation_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the safety observation
    cursor.execute('DELETE FROM safety_observations WHERE safety_observation_id = %s', (observation_id,))
    db.commit()
    flash('Safety observation deleted successfully!', 'danger')
    return redirect(url_for('safety_observations.list_and_create_safety_observations'))

