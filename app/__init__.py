from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)

from app import routes, models, errors

if not app.debug:
    # run 
    # python -m smtpd -n -c DebuggingServer localhost:8025 
    # in another terminal for fake mail server 
    # or set env like
    # export MAIL_SERVER=smtp.googlemail.com
    # export MAIL_PORT=587
    # export MAIL_USE_TLS=1
    # export MAIL_USERNAME=<your-gmail-username>
    # export MAIL_PASSWORD=<your-gmail-password>
    # if app.config['MAIL_SERVER']:
    #     auth = None
    #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #         auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    #     secure = None
    #     if app.config['MAIL_USE_TLS']:
    #         secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
    #         credentials=auth, secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)
    
    # loggin to file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')