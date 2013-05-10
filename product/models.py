from flask.ext.mongoengine.wtf import model_form
from mongoengine import *


class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.pk

    def is_anonymous(self):
        return False


UserForm = model_form(User)


class Bookmark(Document):
    url = StringField(required=True)
    desc = StringField(required=True)
