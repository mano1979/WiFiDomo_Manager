# -*- coding: utf-8 -*-
__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'
from flask import Blueprint, render_template, session, redirect, url_for, \
  request, flash, g, jsonify, abort
from app.utils import requires_login, request_wants_json
from app.search import search as perform_search
from app.wifidomo_manager import verify_password

mod = Blueprint('wifidomos', __name__)

@mod.add('/add/', methods=['POST'])
@requires_login
def add_wifidomo():
  error = None
  location_id = None
  preview = None
  if 'location' in request.args:
    rv = Location.query.filter_by(slug=request.args['location']).first()
    if rv is not None:
      location_id = rv.id
  if request.method == 'POST':
    location_id_id = request.form.get('location_id', type=int)
    if 'preview' in request.form:
      preview = format_creole(request.form[ 'body' ])
    else:
      title = request.form['title']
      body = request.form['body']
      if not body:
        flash(u'Error: you have to enter a location')
      else:
        location = Location.query.get(location_id)
        if location is not None:
          # wifidomo = Wifidomo(g.user, title, body, location)
          # db_session.add(wifidomo)
          # db_session.commit()
          flash(u'Your wifidomo was added')
          return redirect(wifidomo.url)

    return render_template('wifidomos/new.html',
                           categories=Location.query.order_by(Location.name).all(),
                           active_category=location_id,
                           preview=preview)

