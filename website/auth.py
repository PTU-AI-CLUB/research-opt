from flask import Blueprint, render_template, session
from flask import request, redirect, url_for
import pyrebase
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

authb = Blueprint("authb", __name__)

config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "measurementId": os.getenv("measurementId"),
    "databaseURL" : ""
}
firebase = pyrebase.initialize_app(config=config)
auth = firebase.auth()

@authb.route("/signin")
def signin():
    return render_template("signin.html")

@authb.route("/signin_fn", methods=["POST", "GET"])
def signin_fn():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = auth.sign_in_with_email_and_password(email=email,
                                                        password=password)
            session["user"] = email
            return render_template("index.html", user_logged_in=True)
        except Exception as e:
            print(e)
            return "<h1>Something went wrong :( <br> Might be wrong username or password :(</h1>"

@authb.route("/signup")
def signup():
    return render_template("signup.html")

@authb.route("/login_fn", methods=["GET", "POST"])
def login_fn():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            auth.create_user_with_email_and_password(email=email,
                                                     password=password)
            return render_template("signin.html")
        except:
            return "<h1>Something went wrong :( <br> Try again :(</h1>"

@authb.route("/logout")
def logout():
    return "<h1>Logout</h1>"