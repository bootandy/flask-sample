from flask import Flask, render_template
from flask.ext.classy import FlaskView

from product import app
from product.models import *


class UserView(FlaskView):
    def index(self):
        users = User.objects()
        return render_template('users/index.html', users=users)

    def get(self, id):
        user = User.objects.get(id=id)
        return render_template('users/single.html', user=user)


UserView.register(app)
