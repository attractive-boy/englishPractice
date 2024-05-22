# models.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    college = db.Column(db.String(100))
    major = db.Column(db.String(100))
    class_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'college': self.college,
            'major': self.major,
            'class_name': self.class_name,
            'phone': self.phone,
            'email': self.email
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    college = db.Column(db.String(100))
    teacher_number = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    class_responsible = db.Column(db.String(50))

    user = db.relationship('User', backref=db.backref('teacher', uselist=False))
    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'user_id': self.user_id,
            'username': self.user.username,
            'name': self.name,
            'gender': self.gender,
            'college': self.college,
            'teacher_number': self.teacher_number,
            'phone': self.phone,
            'email': self.email,
            'class_responsible': self.class_responsible
        }

class Admin(db.Model):
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Scenario(db.Model):
    __tablename__ = 'scenarios'
    
    scenario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    prompt = db.Column(db.Text)
    difficulty = db.Column(db.Enum('CET4', 'CET6', 'IELTS', 'TOEFL'))
    description = db.Column(db.Text)
    status = db.Column(db.Enum('public', 'private'), default='public')

class StudentStudyRecord(db.Model):
    __tablename__ = 'student_study_records'
    
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.scenario_id'), nullable=False)
    study_date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float)

class TextScore(db.Model):
    __tablename__ = 'text_scores'
    
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    overall_difficulty = db.Column(db.String(50))
    overall_score = db.Column(db.Float)
    vocabulary_difficulty = db.Column(db.Float)
    syntactic_complexity = db.Column(db.Float)
    readability_formula = db.Column(db.Float)
    text_structure = db.Column(db.Float)
    reader_background_knowledge = db.Column(db.Float)
    score_date = db.Column(db.DateTime, default=db.func.current_timestamp())
