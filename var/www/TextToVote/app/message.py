from json import JSONEncoder


class Message:

    def __init__(self, tuple):
        id, phone_number = tuple
        self.id = id
        self.phone_number = phone_number


class MessageEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
