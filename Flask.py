from flask import Flask, request, render_template
from models_Flask import Session, Users, Products

app = Flask(__name__, template_folder='templates')

@app.route('/')
def glavn():
    return render_template('glavn.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    products = Products.query.all()
    if request.method == 'POST':
        message = 'Вы успешно приобрели продукт!'
        return render_template('products.html', message=message)
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_products():
    session = Session()
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        new_product = Products(name=name, price=price)
        session.add(new_product)
        session.commit()
    session.close()
    return render_template('products.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = Session()
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        user = session.query(Users).filter_by(login=login_input, password=password).first()
        if user:
            return render_template('products.html', message=f'Вы вошли успешно')
        else:
            error = 'Неправильный логин или пароль'
            return render_template('login.html', error=error)
    session.close()
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session = Session()
    login = request.form.get('login')
    password = request.form.get('password')
    user = session.query(Users).filter_by(login=login, password=password).first()
    if user:
        session.delete(user)
        session.commit()
        return render_template('logout.html')
    else:
        error = 'Неправильный логин или пароль'
        return render_template('logout.html', error=error)
    session.close()
    return render_template('logout.html')


@app.route('/register', methods=['GET', 'POST'])
def registration():
    session = Session()
    if request.method == 'POST':
        login_input = request.form.get('login')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        if password_1 != password_2:
            error = 'Пароли должны совпадать!'
            return render_template('register.html', error=error)
        existing_user = session.query(Users).filter_by(login=login).first()
        if existing_user:
            error = 'Логин не должен совпадать с логином другого пользователя!'
            return render_template('register.html', error=error)
        new_user = Users(login=login, password=password_2)
        session.add(new_user)
        session.commit()
        return render_template('register.html',
                               message='Регистрация прошла успешно!')
    session.close()
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)