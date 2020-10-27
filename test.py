from flask import Flask, render_template, request, g, session, url_for, redirect
import requests
from flask_debugtoolbar import DebugToolbarExtension
import sys
from threading import Thread
import os
import requests
import time
import mysql.connector
from secret_config import *

app = Flask(__name__)
app.debug = True
app.config.from_object('secret_config')

def connect_db():
    g.mysql_connection=mysql.connector.connect(
            host=['DATABASE_HOST'],
            user=['DATABASE_USER'],
            password=['DATABASE_PASSWORD'],
            database=['DATABASE_NAME']
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

@app.route('/test/')
def testPage():
