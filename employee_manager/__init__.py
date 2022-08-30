from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'bf44ed945ec08fb0b84b1c7b9aed0325'

#engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
engine = create_engine('postgresql://postgres:164Connemara@localhost:5432/employee-manager-db')
#engine = create_engine('postgresql://postgres:164Connemara@db:5432/employee-manager-db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # function name of the route
login_manager.login_message_category = 'info'


# Google Cloud SQL (change this accordingly)---------------------------------------
# PASSWORD ="164Connemara"
# PUBLIC_IP_ADDRESS ="35.223.246.219"
# DBNAME ="employee-manager-db"
# PROJECT_ID ="employee-manager-359205"
# INSTANCE_NAME ="employer-manager"
 
# # configuration
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True



from employee_manager.models import *
Base.metadata.create_all(engine)
if not session.query(Team).first():
	session.add(Team(name='newbies', description='Group of new people who have not joined a team yet'))
	session.commit()
from employee_manager import routes