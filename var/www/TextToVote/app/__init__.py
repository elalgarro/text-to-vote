from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'W0RdP@ss!!33>23'
app.config['MYSQL_DB'] = 'text_to_vote'


from app import views