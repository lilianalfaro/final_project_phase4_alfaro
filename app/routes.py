from flask import render_template
from . import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/safety_observations')
def safety_observations():
    return render_template('safety_observations.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/actions')
def actions():
    return render_template('actions.html')

@app.route('/about')
def about():
    return render_template('about.html')