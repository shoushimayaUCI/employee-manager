from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44ed945ec08fb0b84b1c7b9aed0325'
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # function name of the route
login_manager.login_message_category = 'info'

# Google Cloud SQL (change this accordingly)
PASSWORD ="164Connemara"
PUBLIC_IP_ADDRESS ="35.223.246.219"
DBNAME ="employee-manager-db"
PROJECT_ID ="employee-manager-359205"
INSTANCE_NAME ="employee-manager"
 
# configuration
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
#app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True



from employee_manager.models import Team
if not Team.query.first():
	db.session.add(Team(team_id='newbies', team_name='newbies'))
	db.session.commit()
from employee_manager import routes

