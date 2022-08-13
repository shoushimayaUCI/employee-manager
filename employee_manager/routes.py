from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm import aliased
import secrets
from PIL import Image
import os 

from employee_manager import app, db, bcrypt
from employee_manager.forms import *
from employee_manager.models import *

@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')


@app.route("/home")
@login_required
def home():
    return render_template('home.html', tasks=Task.query.filter_by(person=current_user.email))

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if not form.team_id.data:
            form.team_id.data = "newbie"
        db.session.add(User(username=form.username.data, email=form.email.data, 
            title=form.title.data, team_id=form.team_id.data, password=hashed_password))
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('Logout Successful')
    return redirect(url_for('welcome'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    file_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile-pics', file_name)
    
    # rescaling the size of images we save
    i= Image.open(form_picture)
    i.thumbnail((125, 125))
    i.save(picture_path)
    return file_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.title = form.title.data
        current_user.email = form.email.data
        current_user.team_id = form.team_id.data
        db.session.commit()
        flash('your account has been updated', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.title.data = current_user.title
        form.email.data = current_user.email
        form.team_id.data = current_user.team_id
    image_file = url_for('static', filename='profile-pics/'+current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)


@app.route("/new_task", methods=['GET', 'POST'])
@login_required
def new_task():
    form = NewTaskForm()
    if form.validate_on_submit():
        if not form.person.data:
            form.person.data = current_user.email
        db.session.add(Task(title=form.title.data, description=form.description.data, 
            person=form.person.data))
        db.session.commit()
        flash('The task has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_task.html', form=form)


@app.route("/announcements")
@login_required
def announcements():
    subquery = db.session.query(Announcement).filter(Announcement.team==current_user.team_id)
    return render_template('announcements.html', announcements=subquery.all())


@app.route("/new_announcement", methods=['GET', 'POST'])
@login_required
def new_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        if not form.team.data:
            form.team.data = current_user.team_id
        db.session.add(Announcement(title=form.title.data, author=current_user.email,
            description=form.description.data, team=form.team.data))
        db.session.commit()
        flash('You successfully made an announcement!', 'success')
        return redirect(url_for('announcements'))
    return render_template('new_announcement.html', form=form)


@app.route("/new_team", methods=['GET', 'POST'])
@login_required
def new_team():
    form = TeamForm()
    if form.validate_on_submit():
        db.session.add(Team(team_id=form.team_id.data, team_name=form.team_name.data))
        db.session.commit()
        flash('You successfully made a team!', 'success')
        return redirect(url_for('home'))
    return render_template('new_team.html', form=form)
