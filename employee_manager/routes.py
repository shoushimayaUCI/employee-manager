from flask import render_template, url_for, flash, redirect
from employee_manager import app, db, bcrypt
from employee_manager.forms import RegistrationForm, LoginForm
from employee_manager.models import User

@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.add(User(username=form.username.data, 
            email=form.email.data, title=form.title.data, password=hashed_password))
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
