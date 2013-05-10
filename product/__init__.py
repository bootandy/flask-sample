from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.principal import Principal
from mongoengine import connect


app = Flask(__name__, static_folder='../static', template_folder='templates')

# connect to mongodb
connect('flask_more')

# initalize Flask addons
bcrypt = Bcrypt(app)
Principal(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

# import the views and register them
import views.login_views
import views.views
import views.blueprint_views

app.register_blueprint(views.blueprint_views.bookmarks)
