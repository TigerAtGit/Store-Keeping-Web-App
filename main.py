from flask import Flask, render_template, request, url_for, redirect, flash
from dbservices import dbservices
from datetime import datetime
from datetime import timedelta

app  = Flask(__name__)

db = dbservices()

@app.route('/', methods = ['POST', 'GET'])
def signinpage():
    if request.method == 'POST':
        table = 'Admin'
        username = request.form.get('username')
        password = request.form.get('password')
        data = {'Username':username, 'Password':password}
        val = db.signin_admin(table, data)
        if val == 1:
            return render_template('homepage.html')
        else:
            return render_template('signinpage.html', text = "Invalid credentials!")
    return render_template('signinpage.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
