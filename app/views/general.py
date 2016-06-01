# -*- coding: utf-8 -*-
__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'
from flask import Blueprint, render_template, session, redirect, url_for, \
  request, flash, g, jsonify, abort
from app.utils import requires_login, request_wants_json
from app.search import search as perform_search
from app.wifidomo_manager import verify_password

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
  return render_template('index.html')


@mod.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':

    if not verify_password(request.form['username'], request.form['password']):
      error = 'Invalid login credentials'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('general.index'))
  return render_template('login.html', error=error)


@mod.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('general.login'))


@mod.route('/search/')
def search():
    q = request.args.get('q') or ''
    page = request.args.get('page', type=int) or 1
    results = None
    if q:
        results = perform_search(q, page=page)
        if results is None:
            abort(404)
    return render_template('general/search.html', results=results, q=q)

