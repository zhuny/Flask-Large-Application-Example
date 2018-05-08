

def create_app(config_obj, no_sql=False):
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    # Return the application instance.
    return app
