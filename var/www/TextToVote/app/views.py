from app import app
from flask import  request
from flask_mysqldb import MySQL
from app.submission import  Submission, SubmissionEncoder
from app.message import Message, MessageEncoder
from app.phone_number import PhoneNumber, PhoneNumberEncoder
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
    form = request.form
    resp = MessagingResponse()
    resp.message(parse_message(form))
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
            number = form["From"]
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


def get_or_create_number(body):
    cursor = mysql.connection.cursor()
    number = body["From"]
    cursor.execute("Select * from phone_numbers where phone_number = %s", [str(number)])
    num = cursor.fetchone()
    cursor.close()
    if num is None:
        return num
        # cursor = mysql.connection.cursor()
        # cursor.execute("INSERT INTO phone_numbers(phone_number) VALUES(%s)", [str(number)])
        # resp = mysql.connection.commit()
        # cursor.close()
        # return resp
    else:
        return PhoneNumber(num)


def has_number_voted(number):
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from phone_numbers where phone_number = %s", [str(number)])
    num = cursor.fetchone()
    cursor.close()
    # returns true if number exists
    return num is not None


def parse_message(form):
    cur = mysql.connection.cursor()
    print(form)
    string = form["Body"]
    cur.execute("SELECT * FROM submissions WHERE abrev = %s", [string])
    resp = cur.fetchone()
    cur.close()
    if resp is None:
        return handle_non_vote(form["Body"])
    else:
        if has_number_voted(form["From"]):
            return "Sorry, you can only vote once ;)"
        else:
            log_number(form["From"])
            increment_submission(resp)
            sub = Submission(resp)
            return "Success! You voted for: {}".format(sub.name)


def increment_submission(sub):
    submission = Submission(sub)
    new_count = (int(submission.votes) + 1)
    cur = mysql.connection.cursor()
    cur.execute(
        " UPDATE submissions "
        " SET votes = %s "
        " WHERE id = %s ",
        (new_count, submission.id)
                )
    mysql.connection.commit()
    cur.close()


def handle_non_vote(string):
    if string.upper() == "SUBS":
        return build_subs_list_message(
            get_all_submissions()
        )
    else:
        return "Sorry, your text didn't match any submissions we have. \n" \
               "Text SUBS to see a list of submissions you can vote for."


def get_all_submissions():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM submissions")
    resp = cur.fetchall()
    return map(lambda res: Submission(res), resp)


def build_subs_list_message(subs):
    msg = "VOTE for your favorite film! \n \n"

    for i, submission in enumerate(subs):
        line = "{index}. Text {abrev} for {name} \n".format(
            index=(i + 1),
            abrev=submission.abrev,
            name=submission.name
        )
        msg = msg + line
    return msg


def log_number(number):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO phone_numbers(phone_number) VALUES(%s)", [str(number)])
    mysql.connection.commit()
    cursor.close()
    return
