from app import app
from flask import  request
from flask_mysqldb import MySQL
from app.submission import  Submission, SubmissionEncoder
from app.message import Message, MessageEncoder
from twilio.twiml.messaging_response import MessagingResponse, Message
import json
mysql = MySQL(app)


@app.route('/')
def hello():
    return "Hi Nimo I love you :)"


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

    resp = MessagingResponse()
    resp.message(body + "... in bed ;)")
    return str(resp)


@app.route("/numbers", methods=["GET", "POST"])
def phone_numbers():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM phone_numbers")
        nums = cur.fetchall()
        return json.dumps(nums)
    if request.method == "POST":
        cur = mysql.connection.cursor()
        form = request.form
        try:
            print(str(form))
            number = form["phone_number"]
            cur.execute("INSERT INTO phone_numbers(phone_number) VALUES(%s)", [str(number)])
            mysql.connection.commit()
            cur.close()
            return "did it"
        except Exception as e:
            return str(e)


@app.route("/messages", methods=["GET"])
def messages():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages")
    msgs = cur.fetchall()
    resp = map(lambda res: Message(res), msgs)
    return json.dumps(list(resp), cls=MessageEncoder)

