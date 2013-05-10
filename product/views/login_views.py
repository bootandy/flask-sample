from flask import Flask, Blueprint, current_app, request, session, render_template, redirect, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user,fresh_login_required, AnonymousUser
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed

from product.models import *
from product import app, bcrypt, login_manager


@login_manager.user_loader
def load_user(userid):
    try:
        user = User.objects.get(id=userid)
        return user
    except Exception, e:
        print 'no user'
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
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
