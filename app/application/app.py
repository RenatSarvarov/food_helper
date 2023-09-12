import sqlite3
from flask import Flask, request, g, render_template
import os.path

# UPLOAD_FOLDER = '/static'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','db'])
# приложение#
app = Flask(__name__)
app.config.from_object(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# конфигурация
DATABASE = '/app/application/login_password.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
USE_X_SENDFILE=True

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../../login_password.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('../../login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password FROM 'passwords'
                                               WHERE login = '{}';
                                               ''').format(Login))
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        db_lp.close()
        return render_template('successauth.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('../../login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT INTO 'passwords' VALUES('{}','{}');'''.format(Login, Password)

        cursor_db.execute(sql_insert)

        cursor_db.close()

        db_lp.commit()
        db_lp.close()

        return render_template('successregis.html')

    return render_template('registration.html')

@app.route('/version', methods=['GET', 'POST'])
def version_check():
    if request.method == 'POST':
        userdb = request.form.get('userdb')
        db_lp = sqlite3.connect('../../login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute('''SELECT version FROM 'dbversion' WHERE id='1' '''.format(userdb))
        actualdb = cursor_db.fetchall()
        cursor_db.close()
        try:
            if actualdb[0][0] != userdb:
                return render_template('downloadver.html')
        except:
            return render_template('downloadver.html')
        db_lp.close()
        return render_template('actualver.html')
    return render_template('checkver.html')


#app.route('/download/<path:main>')
# def download_file(main):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],main, as_attachment=True)
# @app.route('/download')
# def get_file():
#     response = make_response(render_template('wait.html'))
#     response.headers['X-Accel-Redirect'] = 'static/db/main.db'
#     return response
# @

if __name__ == "__main__":
    app.run()
