from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44ed945ec08fb0b84b1c7b9aed0325'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # function name of the route
login_manager.login_message_category = 'info'

from employee_manager.models import Team
if not Team.query.first():
	db.session.add(Team(team_id='newbies', team_name='newbies'))
from employee_manager import routes
