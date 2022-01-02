from flask.helpers import url_for,flash
from werkzeug.utils import redirect
from market import app
from flask import render_template
from market.forms import RegistrationForm, LoginForm
from market.models import Item, User
from market import db

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/market')
def product():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                password=form.password1.data,
                                email_address=form.email_address.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('product'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_user=form.password.data):
            login_user(attempted_user)
    return render_template('login.html', form=form)