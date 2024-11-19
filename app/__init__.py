from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from ultralytics import YOLO
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# from app.routes.auth import auth_bp

# app.register_blueprint(auth_bp)

from app import routes, models, commands