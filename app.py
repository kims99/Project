from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from functools import wraps
from sqlalchemy import or_

import pymysql
import secrets
#import os

#dbuser = os.environ.get('DBUSER')
#dbpass = os.environ.get('DBPASS')
#dbhost = os.environ.get('DBHOST')
#dbname = os.environ.get('DBNAME')


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

#Open database connection
dbhost = secrets.dbhost
dbuser = secrets.dbuser
dbpass = secrets.dbpass
dbname = secrets.dbname

db = pymysql.connect(dbhost, dbuser, dbpass, dbname)

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'danger' # sets flash category for the default message 'Please log in to access this page.'


app.config['SECRET_KEY']='SuperSecretKey'
# import os
# = os.environ.get('SECRET_KEY')


# Prevent --> pymysql.err.OperationalError) (2006, "MySQL server has gone away (BrokenPipeError(32, 'Broken pipe')
class SQLAlchemy(_BaseSQLAlchemy):
     def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True
# <-- MWC


app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewUserForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    access = IntegerField('Access: ')
    submit = SubmitField('Create User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UserDetailForm(FlaskForm):
    id = IntegerField('Id: ')
    name = StringField('Name: ', validators=[DataRequired()])
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    access = IntegerField('Access: ')

class AccountDetailForm(FlaskForm):
    id = IntegerField('Id: ')
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

class User(UserMixin, db.Model):
    __tablename__ = 'ksouravong_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer)

    def __init__(self, name, email, username, access=ACCESS['guest']):
        self.id = ''
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = ''
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_user(self):
        return self.access == ACCESS['user']

    def allowed(self, access_level):
        return self.access >= access_level

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)




@login.user_loader
def load_user(id):
    return User.query.get(int(id))  #if this changes to a string, remove int


### custom wrap to determine access level ###
def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated: #the user is not logged in
                return redirect(url_for('login'))

            #user = User.query.filter_by(id=current_user.id).first()

            if not current_user.allowed(access_level):
                flash('You do not have access to this resource.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class ksouravong_vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(15))
    booth_num = db.Column(db.String(10))
    company = db.Column(db.String(50))
    rep = db.Column(db.String(50))
    phone_num = db.Column(db.String(10))
    installed_date = db.Column(db.String(15))
    asset_num = db.Column(db.Integer)
    service = db.Column(db.String(20))
    amount = db.Column(db.String(10))
    paid = db.Column(db.String(3))
    returned = db.Column(db.String(3))

    def __repr__(self):
        return "ID: {0} | Order Date: {1} | Booth #: {2} | Company: {3} | Representative: {4} | Phone Number: {5} | Installed On: {6} | Asset #: {7} | Type of Service: {8} | Bill Amount: {9} | Paid? {10} | Returned? {11}".format(self.vendor_id, self.order_date, self.booth_num, self.company, self.rep, self.phone_num, self.installed_date, self.asset_num, self.service, self.amount, self.paid, self.returned)

class VendorOrderForm(FlaskForm):
    id = IntegerField('Order ID:')
    order_date = StringField('Order Date:', validators=[DataRequired()])
    booth_num = StringField('Booth #:', validators=[DataRequired()])
    company = StringField('Company:', validators=[DataRequired()])
    rep = StringField('Representative:', validators=[DataRequired()])
    phone_num = StringField('Phone Number:', validators=[DataRequired()])
    installed_date = StringField('Installed On:')
    asset_num  = StringField('Asset #:')
    service = StringField('Type of Service:', validators=[DataRequired()])
    amount = StringField('Bill Amount:', validators=[DataRequired()])
    paid = StringField('Paid?')
    returned = StringField('Returned?')



#### Routes ####

# index
@app.route('/')
@app.route('/index')
def index():
    all_vendors = ksouravong_vendors.query.all()
    return render_template('index.html', vendors=all_vendors, pageTitle='Vendor Order Information')

# about
@app.route('/about')
def about():
    return render_template('about.html', pageTitle='About Iowa State Fair Database')

# contact
@app.route('/contact')
def contact():
    return render_template('contact.html', pageTitle='Contact')

# search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = ksouravong_vendors.query.filter(or_(ksouravong_vendors.id.like(search),
                                                ksouravong_vendors.booth_num.like(search),
                                                ksouravong_vendors.company.like(search),
                                                ksouravong_vendors.asset_num.like(search),
                                                ksouravong_vendors.service.like(search),
                                                ksouravong_vendors.paid.like(search),
                                                ksouravong_vendors.returned.like(search))).all()
        return render_template('index.html', vendors=results, pageTitle='Vendor Order', legend="Search Results")
    else:
        return redirect("/")

# add vendor
@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    form = VendorOrderForm()
    if form.validate_on_submit():
        vendor = ksouravong_vendors(id=form.id.data, order_date=form.order_date.data, booth_num=form.booth_num.data, company=form.company.data, rep=form.rep.data, phone_num=form.phone_num.data, installed_date=form.installed_date.data, asset_num=form.asset_num.data, service=form.service.data, amount=form.amount.data, paid=form.paid.data, returned=form.returned.data)
        db.session.add(vendor)
        db.session.commit()
        flash('Order has been successfully created.', 'success')
        return redirect('/')

    return render_template('add_vendor.html', form=form, pageTitle='Add New Order')

#get vendor
@app.route('/vendors/<int:id>', methods=['GET', 'POST'])
def get_vendor(id):
    vendor = ksouravong_vendors.query.get_or_404(id)
    return render_template('vendors.html', form=vendor, pageTitle='Order Details', legend="Order Details")

# registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',  pageTitle='Register | My Flask App', form=form)

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('You are now logged in', 'success')
        return redirect(next_page)
    return render_template('login.html',  pageTitle='Login | My Flask App', form=form)


#logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))


################ GUEST ACCESS FUNCTIONALITY OR GREATER ###################

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.get_or_404(current_user.id)
    form = AccountDetailForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))

    form.name.data = user.name
    form.email.data = user.email

    return render_template('account_detail.html', form=form, pageTitle='Your Account')

################ USER ACCESS FUNCTIONALITY OR GREATER ###################

# dashboard
@app.route('/dashboard')
@requires_access_level(ACCESS['user'])
def dashboard():
    return render_template('dashboard.html', pageTitle='My Flask App Dashboard')

################ ADMIN ACCESS FUNCTIONALITY ###################

# control panel
@app.route('/control_panel')
@requires_access_level(ACCESS['admin'])
def control_panel():
    all_users = User.query.all()
    return render_template('control_panel.html', users=all_users, pageTitle='My Flask App Control Panel')

# user details & update
@app.route('/user_detail/<int:user_id>', methods=['GET','POST'])
@requires_access_level(ACCESS['admin'])
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserDetailForm()
    form.id.data = user.id
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.access.data = user.access
    return render_template('user_detail.html', form=form, pageTitle='User Details')

# update user
@app.route('/update_user/<int:user_id>', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserDetailForm()

    orig_user = user.username # get user details stored in the database - save username into a variable

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data

        new_user = form.username.data

        if new_user != orig_user: # if the form data is not the same as the original username
            valid_user = User.query.filter_by(username=new_user).first() # query the database for the usernam
            if valid_user is not None:
                flash("That username is already taken...", 'danger')
                return redirect(url_for('control_panel'))

        # if the values are the same, we can move on.
        user.username = form.username.data
        user.access = request.form['access_lvl']
        db.session.commit()
        flash('The user has been updated.', 'success')
        return redirect(url_for('control_panel'))

    return redirect(url_for('control_panel'))

# delete user
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_user(user_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted.', 'success')
        return redirect(url_for('control_panel'))

    return redirect(url_for('control_panel'))

# new user
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = NewUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.access = request.form['access_lvl']
        db.session.add(user)
        db.session.commit()
        flash('User has been successfully created.', 'success')
        return redirect(url_for('login'))

    return render_template('new_user.html',  pageTitle='New User | My Flask App', form=form)

#update vendor
@app.route('/vendors/<int:id>/update', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def update_vendor(id):
    vendor = ksouravong_vendors.query.get_or_404(id)
    form = VendorOrderForm()

    if form.validate_on_submit():
        vendor.id = form.id.data
        vendor.order_date = form.order_date.data
        vendor.booth_num = form.booth_num.data
        vendor.company = form.company.data
        vendor.rep = form.rep.data
        vendor.phone_num = form.phone_num.data
        vendor.installed_date = form.installed_date.data
        vendor.asset_num = form.asset_num.data
        vendor.service = form.service.data
        vendor.amount = form.amount.data
        vendor.paid = form.paid.data
        vendor.returned = form.returned.data
        db.session.commit()
        return redirect(url_for('get_vendor', id=vendor.id))

    form.id.data = vendor.id
    form.order_date.data = vendor.order_date
    form.booth_num.data = vendor.booth_num 
    form.company.data = vendor.company 
    form.rep.data = vendor.rep 
    form.phone_num.data = vendor.phone_num  
    form.installed_date.data = vendor.installed_date 
    form.asset_num.data = vendor.asset_num  
    form.service.data = vendor.service 
    form.amount.data = vendor.amount 
    form.paid.data = vendor.paid 
    form.returned.data = vendor.returned  
    return render_template('update_vendor.html', form=form, pageTitle='Update Order', legend="Update An Order")

#delete vendor
@app.route('/delete_vendor/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def delete_vendor(id):
    if request.method == 'POST':
        vendor = ksouravong_vendors.query.get_or_404(id)
        db.session.delete(vendor)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")

# edit order
@app.route('/edit_orders')
@requires_access_level(ACCESS['admin'])
def edit_orders():
    all_vendors = ksouravong_vendors.query.all()
    return render_template('edit_orders.html', vendors=all_vendors, pageTitle='Edit Order')




if __name__ == '__main__':
    app.run(debug=True)
