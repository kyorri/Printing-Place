from flask import render_template, url_for, flash, redirect
from flask_shop import app, db, bcrypt
from flask_shop.forms import SignUpForm, SignInForm, NewProductForm, NewServiceForm, NewUserForm, RemoveForm, ModifyUserForm, ModifyUser2Form, ModifyProductForm, ModifyServiceForm
from flask_shop.models import User, Product, Service, Carts
from flask_login import login_user, logout_user, login_required, current_user
from flask_shop.export import create_pdf

@app.route("/")
@app.route("/home/")
def index():
    return render_template('index.html')


@app.route("/services/")
def services():
    services_provided = Service.query.all()
    return render_template('services.html', s=services_provided)


@app.route("/shop/")
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/contact/")
def contact():
    return render_template('contact.html')


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email_address=form.email_address.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account was created! Log in to your new account..', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email_address=form.email_address.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in succesfully as \'{user.username}\'.', 'success')
            return redirect(url_for('index'))
        else:
            flash(
                f'Login unsuccesful. Please check email address and password!', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout/")
def logout():
    flash(f'Logged out user \'{current_user.username}\'.', 'danger')
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin/")
@login_required
def admin():
    admin = User.query.filter_by(
        email_address='admin@pplace.com', username='admin').first()
    users = User.query.all()
    users.remove(admin)
    products = Product.query.all()
    services = Service.query.all()
    if current_user.is_authenticated:
        if current_user.email_address == admin.email_address and current_user.username == admin.username:
            flash(f'Logged as administrator.', 'success')
            return render_template('admin.html', users=users, products=products, services=services)
    flash(f'Unauthorised access to administration page!', 'danger')
    return redirect(url_for('index'))


@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    form = ModifyUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        current_user.phone_number = form.phone_number.data
        current_user.full_address = form.address.data
        db.session.commit()
    else:
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address
        form.phone_number.data = current_user.phone_number or '-'
        form.address.data = current_user.full_address or '-'
    return render_template('account.html', form=form)


@app.route("/shop/addtocart/<productid>")
@login_required
def buy(productid):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        userid = user.id
        object = Carts.query.filter_by(
            user_id=userid, product_id=productid).first()
        if object:
            object.quantity += 1
            db.session.commit()
        else:
            new_object = Carts(
                user_id=userid, product_id=productid, quantity=1)
            db.session.add(new_object)
            db.session.commit()
        flash('Product added to your shopping cart.', 'info')
    return redirect(url_for('shop'))


@app.route("/shop/del/<productid>")
@login_required
def del_cart(productid):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        userid = user.id
        object = Carts.query.filter_by(
            user_id=userid, product_id=productid).first()
        if object:
            object.quantity -= 1
            if object.quantity == 0:
                flash('Product was removed from your shopping cart.', 'info')
                db.session.delete(object)
            db.session.commit()
    return redirect(url_for('shopping_cart'))


@app.route("/shop/addcart/<productid>")
@login_required
def addcart(productid):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        userid = user.id
        object = Carts.query.filter_by(
            user_id=userid, product_id=productid).first()
        if object:
            object.quantity += 1
            db.session.commit()
        else:
            new_object = Carts(
                user_id=userid, product_id=productid, quantity=1)
            db.session.add(new_object)
            db.session.commit()
    return redirect(url_for('shopping_cart'))


@app.route("/cart/")
@login_required
def shopping_cart():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        cart_items = Carts.query.filter_by(user_id=user.id).all()
        total = 0.0
        products = list()
        for item in cart_items:
            product = dict()
            productid = item.product_id
            product_found = Product.query.filter_by(id=productid).first()
            product['id'] = productid
            product['product_name'] = product_found.product_name
            product['product_description'] = product_found.product_description
            product['product_image'] = product_found.product_image
            product['product_price'] = product_found.product_price
            product['quantity'] = item.quantity
            total += product['quantity'] * product['product_price']
            products.append(product)
        return render_template('cart.html', products=products, total=total)
    else:
        return redirect(url_for('index'))


@app.route('/order/')
@login_required
def order():
    user = User.query.filter_by(username=current_user.username).first()
    cart_items = Carts.query.filter_by(user_id=user.id).all()
    products = list()
    user_ordering = user.username
    address = user.full_address
    for item in cart_items:
        product = dict()
        productid = item.product_id
        product_found = Product.query.filter_by(id=productid).first()
        product['id'] = productid
        product['product'] = product_found.product_name
        product['description'] = product_found.product_description
        product['price'] = product_found.product_price
        product['quantity'] = item.quantity
        products.append(product)
    file_name = create_pdf(products, user_ordering, address)
    return redirect(url_for('static', filename = file_name))


@app.route("/add/<type>/", methods=['GET', 'POST'])
@login_required
def add(type):
    if type == 'product':
        form = NewProductForm()
        if form.validate_on_submit():
            product = Product(product_name=form.product_name.data, product_description=form.product_description.data,
                              product_image=form.product_image.data, product_price=form.product_price.data)
            db.session.add(product)
            db.session.commit()
            flash('Product was added successfully!', 'success')
        return render_template('add.html', form=form, type='Product')
    elif type == 'service':
        form = NewServiceForm()
        if form.validate_on_submit():
            service = Service(service_provided=form.service_description.data)
            db.session.add(service)
            db.session.commit()
            flash('Service was added successfully!', 'success')
        return render_template('add.html', form=form, type='Service')
    elif type == 'user':
        form = NewUserForm()
        if form.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data, email_address=form.email_address.data,
                        password=pw_hash, phone_number=form.phone_number.data, full_address=form.address.data)
            db.session.add(user)
            db.session.commit()
            flash('User was added successfully!', 'success')
        return render_template('add.html', form=form, type='User')
    else:
        return redirect(url_for('admin'))


@app.route("/remove/<type>/", methods=['GET', 'POST'])
@login_required
def remove(type):
    if type == 'product':
        form = RemoveForm()
        entries = Product.query.all()
        form.entry.choices = [(entry.id, entry.product_name)
                              for entry in entries]
        if form.validate_on_submit():
            entry_id = form.entry.data
            entry = Product.query.get(entry_id)
            db.session.delete(entry)
            db.session.commit()
            flash('Product was removed from the database!', 'success')
            return redirect(url_for('admin'))
        return render_template('remove.html', form=form, type='Product')
    elif type == 'service':
        form = RemoveForm()
        entries = Service.query.all()
        form.entry.choices = [(entry.id, entry.service_provided)
                              for entry in entries]
        if form.validate_on_submit():
            entry_id = form.entry.data
            entry = Service.query.get(entry_id)
            db.session.delete(entry)
            db.session.commit()
            flash('Service was removed from the database!', 'success')
            return redirect(url_for('admin'))
        return render_template('remove.html', form=form, type='Service')
    elif type == 'user':
        form = RemoveForm()
        entries = User.query.all()
        form.entry.choices = [(entry.id, entry.username) for entry in entries]
        if form.validate_on_submit():
            entry_id = form.entry.data
            entry = User.query.get(entry_id)
            db.session.delete(entry)
            db.session.commit()
            flash('User was removed from the database!', 'success')
            return redirect(url_for('admin'))
        return render_template('remove.html', form=form, type='User')
    else:
        return redirect(url_for('admin'))
