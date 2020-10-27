#!/usr/bin/env python3.4

from flask import Flask, render_template, request, g, session, url_for, redirect
import requests
from flask_debugtoolbar import DebugToolbarExtension
import mysql.connector
from passlib.hash import bcrypt_sha256

app = Flask(__name__)
app.debug = True
app.config.from_object('secret_config')
toolbar = DebugToolbarExtension(app)

def connect_db():
    g.mysql_connection=mysql.connector.connect(
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            database=app.config['DATABASE_NAME']
    )

    g.mysql_cursor=g.mysql_connection.cursor()
    return g.mysql_cursor

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def homepage():
    return 'hello world'

@app.route('/login/', methods=['GET','POST'])
def login():
    # get form input
    email=str(request.form.get('email'))
    password=str(request.form.get('password'))

    # db connection
    db=get_db()
    db.execute('SELECT email, password, is_admin FROM user WHERE email = %(email)s', {'email':email})
    users=db.fetchall()

    # verify if user exist
    valid_user=False
    for user in users:
        if bcrypt_sha256.verify(password,user[1]):
            valid_user=user
    if valid_user:
        session['user']=valid_user
        return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin/', methods=['GET', 'POST'])
def admin () :
    if request.method == 'GET':
        db = get_db()
        db.execute('SELECT * FROM website;')
        websites = db.fetchall()
        return render_template('admin.html', website=websites)

    url=str(request.form.get('url'))
    name=str(request.form.get('value'))

    db=get_db()
    db.execute('INSERT INTO website(value, timestamp) VALUES ("{}", now());'.format(url))
    g.mysql_connection.commit();
    
    if not session.get('user') or not session.get('user')[2] :
        return redirect(url_for('login'))

    return render_template('admin.html', user = session['user'])

@app.route('/admin/logout/')
def admin_logout () :
    session.clear()
    return redirect(url_for('login'))

#Error 404 methods.
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

