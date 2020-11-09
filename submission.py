from json import JSONEncoder


class Submission:

    def __init__(self, tuple):
        id, name, desc, abrev, votes = tuple
        self.id = id
        self.name = name
        self.desc = desc
        self.abrev = abrev
        self.votes = votes


class SubmissionEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
