from flask import Blueprint, render_template, jsonify
from app.db_connect import get_db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def view_dashboard():
    return render_template('dashboard.html')

@dashboard.route('/api/observations_by_severity')
def observations_by_severity():
    db = get_db()
    cursor = db.cursor()
    query = '''
        SELECT severity, COUNT(*) as count
        FROM safety_observations
        GROUP BY severity
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@dashboard.route('/api/observations_by_category')
def observations_by_category():
    db = get_db()
    cursor = db.cursor()
    query = '''
        SELECT category, COUNT(*) as count
        FROM safety_observations
        GROUP BY category
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@dashboard.route('/api/observations_over_time')
def observations_over_time():
    db = get_db()
    cursor = db.cursor()
    query = '''
        SELECT DATE(date) as observation_date, COUNT(*) as count
        FROM safety_observations
        GROUP BY observation_date
        ORDER BY observation_date
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@dashboard.route('/api/observations_by_employee')
def observations_by_employee():
    db = get_db()
    cursor = db.cursor()
    query = '''
        SELECT CONCAT(e.first_name, ' ', e.last_name) AS employee_name, COUNT(*) as count
        FROM safety_observations s
        JOIN actions a ON s.safety_observation_id = a.safety_observation_id
        JOIN employees e ON a.employee_id = e.employee_id
        GROUP BY e.employee_id
        ORDER BY employee_name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

