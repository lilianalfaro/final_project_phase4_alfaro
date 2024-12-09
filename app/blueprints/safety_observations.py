from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

safety_observations = Blueprint('safety_observations', __name__)

@safety_observations.route('/safety_observations', methods=['GET', 'POST'])
def list_and_create_safety_observations():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new safety observation
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        commodity_type = request.form['commodity_type']
        description = request.form['description']
        severity = request.form['severity']
        status = request.form['status']

        # Insert the new safety observation into the database
        cursor.execute(
            '''
            INSERT INTO safety_observations (date, time, location, commodity_type, description, severity, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (date, time, location, commodity_type, description, severity, status)
        )
        db.commit()

        flash('New safety observation added successfully!', 'success')
        return redirect(url_for('safety_observations.list_and_create_safety_observations'))

    # Fetch all safety observations in dictionary format
    cursor.execute('SELECT * FROM safety_observations')
    all_observations = cursor.fetchall()
    return render_template('safety_observations.html', observations=all_observations)

@safety_observations.route('/update_safety_observation/<int:observation_id>', methods=['GET', 'POST'])
def update_safety_observation(observation_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        commodity_type = request.form['commodity_type']
        description = request.form['description']
        severity = request.form['severity']
        status = request.form['status']

        cursor.execute(
            '''
            UPDATE safety_observations
            SET date = %s, time = %s, location = %s, commodity_type = %s,
                description = %s, severity = %s, status = %s
            WHERE safety_observation_id = %s
            ''',
            (date, time, location, commodity_type, description, severity, status, observation_id)
        )
        db.commit()

        flash('Safety observation updated successfully!', 'success')
        return redirect(url_for('safety_observations.list_and_create_safety_observations'))

    # Fetch observation data to prepopulate the form
    cursor.execute('SELECT * FROM safety_observations WHERE safety_observation_id = %s', (observation_id,))
    current_observation = cursor.fetchone()
    return render_template('update_safety_observation.html', observation=current_observation)

@safety_observations.route('/delete_safety_observation/<int:observation_id>', methods=['POST'])
def delete_safety_observation(observation_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM safety_observations WHERE safety_observation_id = %s', (observation_id,))
    db.commit()

    flash('Safety observation deleted successfully!', 'danger')
    return redirect(url_for('safety_observations.list_and_create_safety_observations'))
