from flask import Flask, render_template, request,redirect,url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app= Flask(__name__)

app.secret_key='flask app'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='mysql_root_password'
app.config['MYSQL_DB']='flasklogin'

mysql=MySQL(app)

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    msg=""
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accounts where username= % s and password= % s', (username,password,) )
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            msg='Logged in successfully !'
            return render_template('index.html',msg=msg)
        else:
            msg='Incorrect username / password !'
    return render_template('login.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('select * from accounts where username=%s',(username,))
        account=cursor.fetchone()

        if account:
            msg='Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Username must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid email address !'
        elif not username or not password or not email:
            msg='Please fill out the form !'
        else:
            cursor.execute('Insert into accounts values(NULL, %s,%s,%s)',(username,password,email,))
            mysql.connection.commit()
            msg='You have successfully registered !'
    elif request.method=='POST':
        msg='Please fill out the form !'
    return render_template('register.html',msg=msg)