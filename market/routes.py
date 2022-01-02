from market.forms import PurchaseItemForm, RegistrationForm, LoginForm, SellItemForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import Item, User
from market import app, db

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def product():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase Item Code
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {purchased_item_object.name} for {purchased_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {purchased_item_object.name} for {purchased_item_object.price}$", category='danger')

        # Sell Item Code
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f"Congratulations! You sold {sold_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {sold_item_object.name}", category='danger')
        return redirect(url_for('product'))
        
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)        
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items ,selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                password=form.password1.data,
                                email_address=form.email_address.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created scuuessfully! You are now loggedIn', category='success')
        return redirect(url_for('product'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in successfully', category='success')
            return redirect(url_for('product'))
        else:
            flash(f'Username and email are not valid', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logoutPage():
    logout_user()
    flash('You are logged out successfully', category='info')
    return redirect(url_for('home'))