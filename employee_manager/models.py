from datetime import datetime
from flask_login import UserMixin, current_user

from employee_manager import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    team_name = db.Column(db.String(50), db.ForeignKey('team.name'), nullable=False, default='newbies')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Team(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(1000))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    person = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.person}')"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50), db.ForeignKey('user.email'), nullable=False)
    description = db.Column(db.Text())
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    team = db.Column(db.String(50), db.ForeignKey('team.name'), nullable=False)