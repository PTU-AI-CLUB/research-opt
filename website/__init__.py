from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .auth import authb
    app.register_blueprint(authb, url_prefix="/")

    app.secret_key = os.getenv("secret_key")

    return app