from flask import Flask

from todolist.config import TestConfig
from todolist.extensions import vue


def create_app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)

    # extensions init
    # VUE init
    vue.init_app(app)

    #view init

    # Return the application instance.
    return app

