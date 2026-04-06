from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class SiteConfig(db.Model):
    __tablename__ = 'site_config'
    
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(50), unique=True, nullable=False)
    config_value = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.config_key,
            'value': self.config_value,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Page(db.Model):
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'content': self.content,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    grade_major = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.String(50), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    github_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    motivation = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    admin_note = db.Column(db.Text, nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    feishu_sent = db.Column(db.Boolean, default=False, nullable=False)
    feishu_error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_id': self.student_id,
            'grade_major': self.grade_major,
            'phone': self.phone,
            'email': self.email,
            'group_id': self.group_id,
            'group_name': self.group_name,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'experience': self.experience,
            'motivation': self.motivation,
            'ip_address': self.ip_address,
            'status': self.status,
            'admin_note': self.admin_note,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'feishu_sent': self.feishu_sent,
            'feishu_error': self.feishu_error,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
