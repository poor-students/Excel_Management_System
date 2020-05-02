import os
import zipfile

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app,send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from EMS.auth import login_required
from EMS.project import project_required

bp = Blueprint('system', __name__, url_prefix='/system')

@bp.route('/import', methods=('POST', 'GET'))
@login_required
@project_required
def import_files():
    if request.method == 'POST':
        if 'excel' not in request.files:
            return redirect(request.url)

        excel_type = request.form['excel_type']
        excel = request.files['excel']

        if excel.filename == '':
            return redirect(request.url)

        if excel:
            filename = secure_filename(excel.filename)
            print(type(excel))
            excel.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{excel_type}_{filename}"))

        return redirect(request.url)

    return render_template('system/import.html')

@bp.route('/export', methods=('POST', 'GET'))
@login_required
@project_required
def export_files():
    if request.method == 'POST':
        excels = map(lambda s:f"{s}.xlsx",request.form['excels'].split(','))

        zip = zipfile.ZipFile(os.path.join(current_app.config['UPLOAD_FOLDER'], "表格.zip"), 'w', zipfile.ZIP_DEFLATED)
        for filename in excels:
            zip.write(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), filename)
        zip.close()

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], "表格.zip", as_attachment=True)


    return render_template('system/export.html')

@bp.route('/users', methods=('POST', 'GET'))
@login_required
@project_required
def users():
    if request.method == 'POST':
        users = []
        for i in range(10):
            users.append(request.form[f'user{i}'])
        print(users)

    return render_template('system/users.html')

@bp.route('/tables', methods=('POST', 'GET'))
@login_required
@project_required
def tables():
    return render_template('system/tables.html')
