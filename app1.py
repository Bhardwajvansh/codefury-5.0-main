from flask import Flask,render_template,request,url_for
from datetime import datetime
import pymysql
import pymysql.cursors


app=Flask(__name__)
app.config['SECRET_KEY'] = '123'

def setup_connection():
    user = 'root'
    DB_PASSWORD = 'welcome123'
    DB_PORT = 3306
    passw = DB_PASSWORD
    host =  'localhost'
    port = DB_PORT
    database = 'startupsupport'
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passw,db=database,cursorclass = pymysql.cursors.DictCursor)
    return conn

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form  :
        username = request.form['username']
        password=request.form['password']
        comp_name = request.form['comp_name']
        address = request.form['address']
        comp_email = request.form['company_email']
        phone = request.form['phone']
        prod = request.form['product_desc']    
        email = request.form['contact_person_email'] 
        support=request.form['Support_needed']
        website=request.form['Website']
        conn = setup_connection()
        print("connected")
        cur = conn.cursor()
        cur.execute('SELECT * FROM startupdetails WHERE username = % s', (username, ))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists !'
        
        else:
            cur.execute('INSERT INTO startupdetails VALUES (NULL, % s,%s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, password,comp_name, address, comp_email, phone, prod, email,support,website ))
            conn.commit()
            msg = 'You have successfully registered !'
        cur.close()
        conn.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        
    return render_template('register1.html', msg = msg)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = setup_connection()
        print("connected")
        cur = conn.cursor()
        cur.execute('SELECT * FROM startupdetails WHERE username = % s', (username, ))
        account = cur.fetchone()
        if account:
            msg = 'Logged in successfully !'
            cur.execute('SELECT * FROM startupdetails WHERE username = % s', (username, ))
            data = cur.fetchone()
            return render_template('display1.html', msg = msg,data=data)
        else:
            msg = 'Incorrect username / password !'
        cur.close()
        conn.close()
    return render_template('login1.html', msg = msg)