from flask import Flask, render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Usuario'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/acceso', methods=["GET", "POST"])
def acceder():
    if request.method == 'POST' and 'txtEmail' in request.form and 'txtPassword':
        _correo = request.form['txtEmail']
        _contrasena = request.form['txtPassword']

        conexion = mysql.connection
        cur = conexion.cursor()
        cur.execute('SELECT * FROM tbl_Usuario WHERE correo = %s AND contrasena = %s', (_correo, _contrasena))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account[0]
            cur.close()

            return render_template('admin.html')
        else:
            return render_template('index.html', mensaje="Usuario incorrecto")

@app.route('/registrar', methods=["GET", "POST"])
def registrar():
    if request.method == 'POST' and 'txtEmail' in request.form and 'txtPassword' and 'txtName' and 'txtLastname':
        _correo = request.form['txtEmail']
        _contrasena = request.form['txtPassword']
        _nombreCompleto = request.form['txtName'] + ' ' + request.form['txtLastname']
        print(_correo)
        print(_contrasena)
        print(_nombreCompleto)
    
        conexion = mysql.connection
        cur = conexion.cursor()
        cur.execute("INSERT INTO tbl_usuario (id_Usuario, Correo, Contrasena, nombre) VALUES (NULL, %s, %s, %s);", (_correo, _contrasena, _nombreCompleto))
        conexion.commit()
        account = cur.lastrowid
        print(account)

        if account:
            session['logueado'] = True

            return render_template('registrado.html')
        else:
            return render_template('registro.html')


if __name__ == '__main__':
    app.secret_key = "david"
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)