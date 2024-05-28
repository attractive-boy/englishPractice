from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import db
from chat import chat_bp
from user import user_bp
from plan import plan_bp
from reports import report_bp
from log import api_log_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize CORS with support for credentials
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = True 
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Enable cross-site cookies

Session(app)
db.init_app(app)

login_manager = LoginManager(app)

app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(report_bp)
app.register_blueprint(api_log_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
