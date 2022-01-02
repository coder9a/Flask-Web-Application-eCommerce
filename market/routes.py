from flask.helpers import url_for,flash
from werkzeug.utils import redirect
from market import app
from flask import render_template
from market.forms import RegistrationForm
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
                                password_hash=form.password1.data,
                                email_address=form.email_address.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('product'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)