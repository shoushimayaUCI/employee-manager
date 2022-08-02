from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44ed945ec08fb0b84b1c7b9aed0325'

from employee_manager import routes