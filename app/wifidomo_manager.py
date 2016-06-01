#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'
# ==============================================================================
#
#  App name: wifidomo_manager.py
#
#  Target system:  Linux
#
#  Description:
#
#
# ==============================================================================
#
# Todo:
#
# ===========================================================================
# Imports
# ===========================================================================
import sys
import getopt
import threading
import paramiko
import subprocess
import time
import os
from datetime import datetime
from flask import Flask, render_template, url_for, request, g, flash, redirect, jsonify, session
from flask.ext.navigation import Navigation
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.contrib.fixers import ProxyFix

# ===========================================================================
# Global settings
# ===========================================================================
# Setup Flask
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
nav = Navigation(app)

users = {
  "Admin": generate_password_hash("WiFiDomo")
}

app.config['USERNAME'] = 'Admin'
app.config['PASSWORD'] = generate_password_hash("WiFiDomo")

# Website navigation:
nav.Bar('top', [
  nav.Item('Home', 'index'),
  nav.Item('Add', 'index'),
  nav.Item('Overview', 'index'),
  nav.Item('About', 'index')
])

'''
# ===========================================================================
# Handlers
# ===========================================================================
'''

@app.route('/')
def index():
  return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':

    if not verify_password(request.form['username'], request.form['password']):
      error = 'Invalid login credentials'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('index'))
  return render_template('login.html', error=error)


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('index'))


#from flask_website.database import User, db_session
from flask_website import utils

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
