from flask import Flask, request, render_template
import sqlite3


connection = sqlite3.connect('Flask.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
login TEXT UNIQUE,
password TEXT
)
''')
connection.commit()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def glavn():
    return render_template('glavn.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        cursor.execute('SELECT * FROM Users WHERE login = ? AND password = ?',
                       (login_input, password))
        user = cursor.fetchone()
        if user:
            return render_template('login.html', message=f'Вы вошли как {login_input}')
        else:
            error = 'Неправильный логин или пароль'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    login_input = request.form.get('login')
    password = request.form.get('password')
    cursor.execute('DELETE FROM Users WHERE login = ? AND password = ?',
                   (login_input, password))
    connection.commit()
    return render_template('logout.html')


@app.route('/registr', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        if password_1 != password_2:
            error = 'Пароли должны совпадать!'
            return render_template('registr.html', error=error)
        cursor.execute('SELECT * FROM Users WHERE login = ?', (login_input,))
        if cursor.fetchone():
            error = 'Логин не должен совпадать с логином другого пользователя!'
            return render_template('registr.html', error=error)
        cursor.execute('INSERT INTO Users (login, password) VALUES (?, ?)',
                       (login_input, password_2))
        connection.commit()
        return render_template('registr.html', message='Регистрация прошла успешно!')
    return render_template('registr.html')


if __name__ == '__main__':
    app.run(debug=True)