import os
import secrets
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect, text

from config import config
from defaults import DEFAULT_GITHUB_URL
from models import db, Page, Application


def ensure_application_schema():
    inspector = inspect(db.engine)
    if 'applications' not in inspector.get_table_names():
        return

    columns = {column['name'] for column in inspector.get_columns('applications')}
    migration_sql = []

    if 'status' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending'"
        )
    if 'admin_note' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN admin_note TEXT NULL"
        )
    if 'processed_at' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN processed_at DATETIME NULL"
        )
    if 'action_token' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN action_token VARCHAR(64) NULL"
        )
    if 'result_type' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN result_type VARCHAR(20) NULL"
        )
    if 'review_group_info' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN review_group_info TEXT NULL"
        )
    if 'result_email_links' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN result_email_links TEXT NULL"
        )
    if 'result_email_image_url' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN result_email_image_url VARCHAR(255) NULL"
        )
    if 'last_email_type' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN last_email_type VARCHAR(30) NULL"
        )
    if 'last_email_sent' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN last_email_sent BOOLEAN NOT NULL DEFAULT FALSE"
        )
    if 'last_email_error' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN last_email_error TEXT NULL"
        )
    if 'last_email_sent_at' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN last_email_sent_at DATETIME NULL"
        )
    if 'feishu_message_id' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN feishu_message_id VARCHAR(120) NULL"
        )
    if 'feishu_open_message_id' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN feishu_open_message_id VARCHAR(120) NULL"
        )
    if 'feishu_delivery_mode' not in columns:
        migration_sql.append(
            "ALTER TABLE applications ADD COLUMN feishu_delivery_mode VARCHAR(20) NULL"
        )

    for sql in migration_sql:
        db.session.execute(text(sql))

    if migration_sql:
        db.session.commit()

    missing_tokens = Application.query.filter(
        (Application.action_token.is_(None)) | (Application.action_token == '')
    ).all()
    if missing_tokens:
        for application in missing_tokens:
            application.action_token = secrets.token_hex(24)
        db.session.commit()


def ensure_join_page_defaults():
    join_page = Page.query.filter_by(slug='join').first()
    if not join_page or not isinstance(join_page.content, dict):
        return

    form = dict(join_page.content.get('form') or {})
    current_default = form.get('defaultGithubUrl')
    if current_default not in (None, '', DEFAULT_GITHUB_URL, 'https://github.com'):
        return

    form['defaultGithubUrl'] = ''
    join_page.content = {
        **join_page.content,
        'form': form
    }
    db.session.commit()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    JWTManager(app)
    
    from routes.api import api_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    with app.app_context():
        db.create_all()
        ensure_application_schema()
        ensure_join_page_defaults()
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error', 'message': str(error)}), 500
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Xingyu CMS API is running'})

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['APP_HOST'],
        port=app.config['APP_PORT'],
        debug=app.config['DEBUG']
    )
