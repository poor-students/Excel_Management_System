import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from EMS.auth import login_required

bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def select():
    if request.method == 'POST':
        project_id = request.form['projects']

        session['project_id'] = project_id
        return redirect(url_for('system.import_files'))

    return render_template('project/select.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        project_name = request.form['project_name']

        return redirect(url_for('project.select'))

    return render_template('project/create.html')

@bp.route('/close_project')
def close_project():
    del session['project_id']
    return redirect(url_for('project.select'))

@bp.before_app_request
def load_using_project():
    project_id = session.get('project_id')

    if project_id is None:
        g.project_id = None
    else:
        g.project_id = project_id

def project_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.project_id is None:
            return redirect(url_for('project.select'))

        return view(**kwargs)

    return wrapped_view
