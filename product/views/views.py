from flask import Flask, Blueprint, current_app, request, session, render_template, redirect, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user,fresh_login_required, AnonymousUser
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed

from product.models import *
from product import app, bcrypt, login_manager


@app.route('/')
def home_page():
    online_users = User.objects()
    return render_template('index.html', online_users=online_users)


@app.route("/secret")
@fresh_login_required # Fresh login ensures a revent login otherwise use: @login_required
def secret():
    return render_template("secret.html")


# cool routes alternative :-)
@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        print rule
        print rule.endpoint
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and rule.defaults is not None and len(rule.defaults) >= len(rule.arguments):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)
