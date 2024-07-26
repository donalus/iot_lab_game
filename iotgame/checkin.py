from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from iotgame.auth import login_required
from iotgame.db import get_db

bp = Blueprint('checkin', __name__)

@bp.route('/', methods = ('GET', 'POST'))
def index():
    if request.method == 'POST':
        team_number = request.form['team_number']
        client_address = request.form['client_address']
        error = None

        if not team_number:
            error = 'Team number is required.'
        if not client_address:
            error = 'Client address is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO checkins (team_number, client_address)'
                ' VALUES (?, ?)',
                (team_number, client_address)
            )
            db.commit()
            return redirect(url_for('checkin.index'))
    db = get_db()
    checkins = db.execute(
        'SELECT id, created, team_number, client_address'
        ' FROM checkins '
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('checkin/index.html', checkins=checkins, client_address=request.remote_addr)

@bp.route('/admin', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        confirm = request.form['confirm']
        error = None

        if not confirm or (confirm != 'yes' and confirm != 'Yes' and confirm != 'y' and confirm != 'Y'):
            error = 'You must confirm that you want to clear the database.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'DELETE FROM checkins'
            )
            db.commit()
            return redirect(url_for('checkin.index'))

    return render_template('checkin/admin.html')
