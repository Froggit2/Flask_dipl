from flask import Flask, request, render_template
import sqlite3

connection = sqlite3.connect('Flask.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users
(
id INTEGER PRIMARY KEY,
login TEXT,
email TEXT,
password TEXT
)
''')


app = Flask(__name__, template_folder='templates')

@app.route('/')
def glavn():
    return render_template('glavn.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('email')
        cursor.execute('SELECT login * FROM Users')
        login_db = cursor.fetchall()
        cursor.execute('SELECT password * FROM Users')
        pass_db = cursor.fetchall()
        cursor.execute('SELECT email * FROM Users')
        email_db = cursor.fetchall()
        if login == login_db and password == pass_db and email == email_db:
            return render_template('login.html')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    pass


@app.route('/registr', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('email')
        cursor.execute('SELECT login * FROM Users')
        login_db = cursor.fetchall()
        if login_db == login:
            error = 'Логин не должен совпадать с логином другого пользователя!'
            return render_template('registr.html', error=error)
        cursor.execute('SELECT email * FROM Users')
        email_db = cursor.fetchall()
        if email_db == email:
            error = 'Нельзя зарегестрировать на одну почту два аккаунта!'
            return render_template('registr.html', error=error)
        # #
        # cursor.execute('SELECT password * FROM Users')
        # pass_db = cursor.fetchall()
        # if pass_db != password:
        #     error = 'Пароли должны совпадать!'
        #     return render_template('registr.html', error=error)
        # #
        cursor.execute('INSERT INTO Users (login, email, password) VALUES(?, ?, ?)',
                       (login, password))
        connection.commit()
        return render_template('registr.html')
    return render_template('registr.html')


if __name__ == '__main__':
    app.run(debug=True)