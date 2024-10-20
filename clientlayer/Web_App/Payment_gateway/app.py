from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from routes import *

if __name__ == "__main__":
    db.create_all()  # Create database tables
    app.run(debug=True)