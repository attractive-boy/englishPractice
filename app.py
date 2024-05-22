from flask import Flask
from flask_cors import CORS
from flask_session import Session
from models import db
from auth import auth_bp
from student import student_bp
from teacher import teacher_bp
from scenario import scenario_bp
from study_record import study_record_bp
from text_score import text_score_bp

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

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(student_bp, url_prefix='/api')
app.register_blueprint(teacher_bp, url_prefix='/api')
app.register_blueprint(scenario_bp, url_prefix='/api')
app.register_blueprint(study_record_bp, url_prefix='/api')
app.register_blueprint(text_score_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
