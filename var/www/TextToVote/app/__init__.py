from flask import Flask
import os
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_ROOT_PASSWORD")
app.config['MYSQL_DB'] = 'text_to_vote'


from app import views