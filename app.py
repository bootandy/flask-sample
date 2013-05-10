from flask import Flask, current_app, request, session, render_template, redirect
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user,fresh_login_required, AnonymousUser
from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, Required, Email
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed
from flask.ext.bcrypt import Bcrypt
from mongoengine import connect

from models import *


connect('flask_more')

app = Flask(__name__)
Principal(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        user = User.objects.get(id=userid)
        return user
    except Exception, e:
        print 'no user'
        return None


@app.route('/')
def home_page():
    online_users = User.objects()
    return render_template('index.html', online_users=online_users)


@app.route("/secret")
@fresh_login_required # Fresh login ensures a revent login otherwise use: @login_required
def secret():
    return render_template("secret.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.form)

        # Validate form input
        if form.validate_on_submit():
            try:
                # Retrieve the user from the hypothetical datastore
                user = User.objects.get(email=form.email.data)

                # if passwords match
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)

                    # Tell Flask-Principal the identity changed
                    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

                    return redirect(request.args.get('next') or '/')
            except Exception, e:
                pass

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.form)

        # Validate form input
        if form.validate_on_submit():
            # Retrieve the user from the hypothetical datastore
            form.password.data = bcrypt.generate_password_hash(form.password.data)
            form.save()
            login_user(form.instance)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(), identity=Identity(form.instance.id))

            return redirect(request.args.get('next') or '/')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')


if __name__ == "__main__":
    app.secret_key = "yeah, not actually a secret"
    app.debug = True

    if app.config['DEBUG']:
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), 'static')
        })
    app.run()
