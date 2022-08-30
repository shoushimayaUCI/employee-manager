from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from employee_manager import Base, login_manager, session


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    title = Column(String(50), unique=False, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    team_name = Column(String(50), ForeignKey('Team.name'), nullable=False, default='newbies')
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Team(Base):
    __tablename__ = 'Team'
    name = Column(String(50), primary_key=True)
    description = Column(String(1000))


class Task(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(Text())
    person = Column(String(120), ForeignKey('User.email'), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.person}')"


class Announcement(Base):
    __tablename__ = 'Announcement'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50), ForeignKey('User.email'), nullable=False)
    description = Column(Text())
    date_post = Column(DateTime, nullable=False, default=datetime.utcnow)
    team = Column(String(50), ForeignKey('Team.name'), nullable=False)