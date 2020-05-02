import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        email = request.form['email']
        true_name = request.form['true_name']
        invitation_code = request.form['invitation_code']

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session.clear()
        session['user'] = username
        return redirect(url_for('project.select'))

    return render_template('auth/login.html')

@bp.route('/change_password', methods=('GET', 'POST'))
def change():
    if request.method == 'POST':
        password = request.form['password']
        verify_password = request.form['verify_password']

        return redirect(url_for('auth.logout'))

    return render_template('auth/change.html')

@bp.route('/reset', methods=('GET', 'POST'))
def reset():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        return redirect(url_for('auth.login'))

    return render_template('auth/reset.html')

@bp.before_app_request
def load_logged_in_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        g.user = user

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

