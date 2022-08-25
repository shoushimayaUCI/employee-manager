from flask import render_template, url_for, flash, redirect, request, make_response
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm import aliased
import secrets
from PIL import Image
import os 
from flask_restful import Resource

from employee_manager import app, db, bcrypt, api
from employee_manager.forms import *
from employee_manager.models import *

class welcome(Resource):
    def get(self):
        return make_response(render_template('welcome.html'))


class home(Resource):
    @login_required
    def get(self):
        return make_response(render_template('home.html', tasks=Task.query.filter_by(person=current_user.email)))

class about(Resource):
    def get(self):
        return make_response(render_template('about.html', title='About'))


class register(Resource):
    def get(self):
        return make_response(render_template('register.html', title='Register', form=RegistrationForm()))

    def post(self):
        form=RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if not form.team_name.data:
                form.team_name.data = "newbies"
            db.session.add(User(username=form.username.data, email=form.email.data, 
                title=form.title.data, team_name=form.team_name.data, password=hashed_password))
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return make_response(redirect(url_for('login')))
        return make_response(render_template('register.html', title='Register', form=form))


class login(Resource):
    def get(self):
        return make_response(render_template('login.html', title='Login', form=LoginForm()))

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return make_response(redirect(next_page) if next_page else redirect(url_for('home')))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return make_response(render_template('login.html', title='Login', form=form))


class logout(Resource):
    @login_required
    def get(self):
        logout_user()
        flash('Logout Successful')
        return make_response(redirect(url_for('welcome')))


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


class account(Resource):
    @login_required
    def get(self):
        form = UpdateAccountForm()
        image_file = url_for('static', filename='profile-pics/'+current_user.image_file)
        return make_response(render_template('account.html', title='Account', form=form, image_file=image_file))

    @login_required
    def post(self):
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.title = form.title.data
            current_user.email = form.email.data
            current_user.team_name = form.team_name.data
            db.session.commit()
            flash('your account has been updated', category='success')
            return make_response(redirect(url_for('account')))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.title.data = current_user.title
            form.email.data = current_user.email
            form.team_name.data = current_user.team_name
        image_file = url_for('static', filename='profile-pics/'+current_user.image_file)
        return make_response(render_template('account.html', title='Account', form=form, image_file=image_file))


class new_task(Resource):
    @login_required
    def get(self):
        return make_response(render_template('new_task.html', form=NewTaskForm()))

    @login_required
    def post(self):
        form = NewTaskForm()
        if form.validate_on_submit():
            if not form.person.data:
                form.person.data = current_user.email
            db.session.add(Task(title=form.title.data, description=form.description.data, 
                person=form.person.data))
            db.session.commit()
            flash('The task has been created!', 'success')
            return make_response(redirect(url_for('home')))
        return make_response(render_template('new_task.html', form=form))


class announcements(Resource):
    @login_required
    def get(self):
        subquery = db.session.query(Announcement).filter(Announcement.team==current_user.team_name)
        return make_response(render_template('announcements.html', announcements=subquery.all()))


class new_announcement(Resource):
    @login_required
    def get(self):
        return make_response(render_template('new_announcement.html', form=AnnouncementForm()))

    @login_required
    def post(self):
        form = AnnouncementForm()
        if form.validate_on_submit():
            if not form.team.data:
                form.team.data = current_user.team_name
            db.session.add(Announcement(title=form.title.data, author=current_user.email,
                description=form.description.data, team=form.team.data))
            db.session.commit()
            flash('You successfully made an announcement!', 'success')
            return make_response(redirect(url_for('announcements')))
        return make_response(render_template('new_announcement.html', form=form))


class new_team(Resource):
    @login_required
    def get(self):
        return make_response(render_template('new_team.html', form=TeamForm()))

    @login_required
    def post(self):
        form = TeamForm()
        if form.validate_on_submit():
            db.session.add(Team(name=form.name.data, description=form.description.data))
            db.session.commit()
            flash('You successfully made a team!', 'success')
            return make_response(redirect(url_for('home')))
        return make_response(render_template('new_team.html', form=form))


class teams(Resource):
    @login_required
    def get(self):
        return make_response(render_template('teams.html',teams=Team.query.all()))


api.add_resource(welcome, "/")
api.add_resource(register, '/register')
api.add_resource(about, '/about')
api.add_resource(home, '/home')
api.add_resource(login, '/login')
api.add_resource(logout, '/logout')
api.add_resource(account, '/account')
api.add_resource(new_task, '/new_task')
api.add_resource(announcements, '/announcements')
api.add_resource(new_announcement, '/new_announcement')
api.add_resource(new_team, '/new_team')
api.add_resource(teams, '/teams')