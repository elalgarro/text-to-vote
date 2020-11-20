from flask import Flask, request
from flask_mysqldb import MySQL
from submission import Submission, SubmissionEncoder
import json
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'W0RdP@ss!!33>23'
app.config['MYSQL_DB'] = 'text_to_vote'
mysql = MySQL(app)

@app.route('/')
def hello():
    return "FILM FESTIVAL: WOOO"


@app.route("/submissions", methods=['GET', 'POST'])
def submissions():
    if request.method == "POST":
        return submissions_post(request.form)
    else:
        return submissions_index()


def submissions_index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM submissions")
    resp = cur.fetchall()
    subs = map(lambda res: Submission(res), resp)
    return json.dumps(list(subs), cls=SubmissionEncoder)


def submissions_post(form):
    cur = mysql.connection.cursor()
    details = request.form
    name = details["name"]
    desc = details["description"]
    abrev = details["abrev"]
    cur.execute("INSERT INTO submissions(name, description, abrev) VALUES(%s, %s, %s)", (name, desc, abrev))
    mysql.connection.commit()
    cur.close()
    return 'success'


@app.route("/submissions/<id>", methods=['DELETE'])
def delete_submission():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM submissions where id=%s", id)
    return 'success'


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')

