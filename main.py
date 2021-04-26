from flask import Flask, render_template, request, url_for, redirect, flash
from dbservices import dbservices
from datetime import datetime
from datetime import timedelta

app  = Flask(__name__)
app.secret_key = "super_secret_key"

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

@app.route('/display', methods = ['POST', 'GET'])
def display():
    # if request.method == 'POST':
    table = 'Products'

    cat1 = db.fetch_item_records(table, 'category 1')
    cat2 = db.fetch_item_records(table, 'category 2')
    cat3 = db.fetch_item_records(table, 'category 3')
    cat4 = db.fetch_item_records(table, 'category 4')

    return render_template('display.html', record1=cat1, record2=cat2, record3=cat3, record4=cat4)
    # return render_template('display.html')

@app.route('/additem', methods = ['POST', 'GET'])
def additem():
    if request.method == 'POST':
        table = 'Products'
        pname = request.form.get('pname')
        category = request.form.get('category')
        price = request.form.get('price')
        stock = request.form.get('stock')
        desc = request.form.get('desc')
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        data = {'PName': pname, '`Category`': category, 'Price': price, 'Stock': stock, '`Description`': desc, '`Date`': date}
        db.add_record(table, data)
        flash('New item added :)')
        return redirect('/additem')
    else:
        categories = db.fetch_column_data('Category', ['Id', '`Name`'])
        return render_template('additem.html', categories = categories)

@app.route('/deleteitem', methods = ['POST', 'GET'])
def deleteitem():
    if request.method == 'POST':
        table = 'Products'
        productid = request.form.get('productid')
        db.delete_record(table, productid)
        return render_template('deleteitem.html', text = 'Item deleted successfully!')
    return render_template('deleteitem.html')