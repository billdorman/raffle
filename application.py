from flask import Flask
from flask_cors import CORS
from extensions import db, ma, jwt, login_manager, scheduler
from config import const as CONSTANTS
from services import scheduler_service
from web import web_auth
from web import web_items
from web import web_search
from web import web_checkout
from web import web_admin_items
from web import drawing
from web import web_tickets
import logging

log = logging.getLogger()

logHandler = logging.FileHandler(CONSTANTS.LOG_FILE_NAME)
logHandler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
log.addHandler(logHandler)

log.warning("\n\n                                    ********************\n                                    "
            "Starting Raffle Web API\n                                    ********************\n")

loggingLevel = logging.getLevelName(CONSTANTS.LOGGING_LEVEL)
if type(loggingLevel).__name__ == 'int':
    log.setLevel(loggingLevel)
else:
    log.error(
        f"Unable to use config.const.py logging level \"{CONSTANTS.LOGGING_LEVEL}\" - not recognized as a predefined logging level.")
log.warning(f"Logging is set to level: {log.level} - {logging.getLevelName(log.level)}")


def create_app():
    log.info("create_app. Preparing to setup Flask")
    application = Flask(__name__)
    CORS(application)
    configure_app(application)
    register_extensions(application)
    initialize_scheduler(application)
    return application


def configure_app(application):
    log.info("Configuring app")
    application.config['SQLALCHEMY_DATABASE_URI'] = CONSTANTS.DB_CONNECTION_STRING
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SECRET_KEY'] = CONSTANTS.SECRET
    application.config['JWT_SECRET_KEY'] = CONSTANTS.JWT_SECRET
    application.config['JWT_BLACKLIST_ENABLED'] = True
    application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['refresh']


def register_extensions(application):
    log.info("Registering extensions")
    db.init_app(application)
    ma.init_app(application)
    jwt.init_app(application)
    login_manager.init_app(application)
    login_manager.login_view = 'web_auth.login_get'


def initialize_scheduler(application):
    scheduler.api_enabled = True
    scheduler.init_app(application)
    scheduler.start()
    scheduler_service.init_scheduler_service(application)

def register_blueprints(application):
    log.info("Registering blueprints")
    application.register_blueprint(web_items, url_prefix='/')
    application.register_blueprint(web_auth, url_prefix='/auth')
    application.register_blueprint(web_search, url_prefix='/search')
    application.register_blueprint(web_checkout, url_prefix='/checkout')
    application.register_blueprint(web_admin_items, url_prefix='/admin/items')
    application.register_blueprint(drawing, url_prefix='/admin/drawing')
    application.register_blueprint(web_tickets, url_prefix='/tickets')


log.info("Preparing to call create_app")
application = create_app()
register_blueprints(application)




# Start the flask server
if __name__ == '__main__':
    application.run(debug=True, use_reloader=False)