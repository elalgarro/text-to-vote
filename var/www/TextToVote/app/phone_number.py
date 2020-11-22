from json import JSONEncoder


class PhoneNumber:

    def __init__(self, tuple):
        id, phone_number = tuple
        self.id = id
        self.phone_number = phone_number


class PhoneNumberEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
