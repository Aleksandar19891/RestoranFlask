from flask import Flask, render_template, request, session, redirect, url_for
import flask_bootstrap
import flask
from flask_mysqldb import MySQL
import yaml

aplikacija = Flask(__name__)
aplikacija.secret_key = 'asldfjhulr#89347#579d^^ajh'
flask_bootstrap.Bootstrap(aplikacija)

# Configure DB
db = yaml.load(open('baza.yaml'))
aplikacija.config['MYSQL_HOST'] = db['mysql_host']
aplikacija.config['MYSQL_USER'] = db['mysql_user']
aplikacija.config['MYSQL_PASSWORD'] = db['mysql_password']
aplikacija.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(aplikacija)


@aplikacija.route('/')
def index():
    return render_template('index.html')



@aplikacija.route('/hrana')
def hrana():
    return render_template('hrana.html')

@aplikacija.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('username') is None:
            cursor = mysql.connection.cursor()
            us_ime = request.form.get('username')
            sifra = request.form.get('sifra')
            if cursor.execute('SELECT * FROM admin where username = %s and sifra = %s', [us_ime, sifra])>0:
                admin = cursor.fetchone()
                session['ulogovan'] = True
                session['username'] = admin[1]
                mysql.connection.commit()

                return render_template('index.html')
            else:
                return render_template('login.html')
        else:
            return render_template('index.html')
    else:
        return render_template('login.html')

@aplikacija.route('/registracija', methods=['POST', 'GET'])
def registracija():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        ime = request.form.get('username')
        email = request.form.get('email')
        sifra = request.form.get('sifra')
        potvrda_sifre = request.form.get('potvrda')
        if sifra == potvrda_sifre:
            if cursor.execute('SELECT * from admin where email = %s', [email]) == 0:
                cursor.execute('INSERT INTO admin(username,email,sifra)  VALUES(%s,%s,%s)',
                               [ime,email,sifra])
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('index'))
            else:
                return render_template('registracija.html')
        else:
            return render_template('registracija.html')
    else:
        return render_template('registracija.html')

@aplikacija.route('/logout', methods=['POST', 'GET'])
def logout():
    if session.get('username') is not None:
        session.pop('username')
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@aplikacija.route('/zabava')
def zabava():
    return render_template('zabava.html')

@aplikacija.route('/pice')
def pice():
    return render_template('pice.html')

@aplikacija.route('/prostorije')
def prostorije():
    return render_template('prostorije.html')




if __name__ == '__main__':
    aplikacija.run(debug=True)
