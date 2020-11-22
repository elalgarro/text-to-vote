from json import JSONEncoder


class Vote:

    def __init__(self, tuple):
        submission_id, phone_number_id, round_number = tuple
        self.submission_id = submission_id
        self.phone_number_id = phone_number_id
        self.round_number = round_number


class VoteEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
