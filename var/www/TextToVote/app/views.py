from app import app
from flask import  request
from flask_mysqldb import MySQL
from app.submission import  Submission, SubmissionEncoder
from twilio import twiml
import json
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

@app.route("/message", methods=['POST'])
def message():
    number = request.form["From"]
    body = request.form["Body"]
    resp = twiml.Response()
    resp.message(body + "... in bed ;)")
    return str(resp)
