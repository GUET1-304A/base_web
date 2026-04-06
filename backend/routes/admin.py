import copy
import os
import uuid
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, SiteConfig, Page, AdminUser, Application
from defaults import DEFAULT_SITE_CONFIG, DEFAULT_PAGES

admin_bp = Blueprint('admin', __name__)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def reset_configs_to_default():
    existing_configs = {config.config_key: config for config in SiteConfig.query.all()}

    for key, value in DEFAULT_SITE_CONFIG.items():
        config = existing_configs.get(key)
        if config:
            config.config_value = copy.deepcopy(value)
        else:
            db.session.add(SiteConfig(config_key=key, config_value=copy.deepcopy(value)))

    for key, config in existing_configs.items():
        if key not in DEFAULT_SITE_CONFIG:
            db.session.delete(config)


def reset_pages_to_default():
    existing_pages = {page.slug: page for page in Page.query.all()}

    for slug, page_data in DEFAULT_PAGES.items():
        page = existing_pages.get(slug)
        if page:
            page.title = page_data['title']
            page.content = copy.deepcopy(page_data['content'])
        else:
            db.session.add(Page(
                slug=slug,
                title=page_data['title'],
                content=copy.deepcopy(page_data['content'])
            ))

    for slug, page in existing_pages.items():
        if slug not in DEFAULT_PAGES:
            db.session.delete(page)


@admin_bp.route('/login', methods=['POST'])
def login():
    """管理员登录"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = AdminUser.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'success': True,
        'token': access_token,
        'user': user.to_dict()
    })


@admin_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = int(get_jwt_identity())
    user = AdminUser.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())


@admin_bp.route('/config', methods=['GET'])
@jwt_required()
def get_config():
    """获取站点配置（管理端）"""
    configs = SiteConfig.query.all()
    
    result = {}
    for config in configs:
        result[config.config_key] = config.config_value
    
    return jsonify(result)


@admin_bp.route('/config', methods=['PUT'])
@jwt_required()
def update_config():
    """更新站点配置"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for key, value in data.items():
        config = SiteConfig.query.filter_by(config_key=key).first()
        if config:
            config.config_value = value
        else:
            config = SiteConfig(config_key=key, config_value=value)
            db.session.add(config)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '配置保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/config/<key>', methods=['PUT'])
@jwt_required()
def update_config_key(key):
    """更新单个配置项"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    config = SiteConfig.query.filter_by(config_key=key).first()
    if config:
        config.config_value = data
    else:
        config = SiteConfig(config_key=key, config_value=data)
        db.session.add(config)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'{key} 配置保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/pages', methods=['GET'])
@jwt_required()
def get_pages():
    """获取所有页面列表"""
    pages = Page.query.all()
    return jsonify([p.to_dict() for p in pages])


@admin_bp.route('/pages', methods=['POST'])
@jwt_required()
def create_page():
    """创建新页面"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    slug = data.get('slug')
    if not slug:
        return jsonify({'error': 'Slug is required'}), 400
    
    existing = Page.query.filter_by(slug=slug).first()
    if existing:
        return jsonify({'error': 'Page with this slug already exists'}), 400
    
    page = Page(
        slug=slug,
        title=data.get('title', slug.replace('-', ' ').title()),
        content=data.get('content', {})
    )
    
    try:
        db.session.add(page)
        db.session.commit()
        return jsonify({'success': True, 'message': '页面创建成功', 'page': page.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/pages/<slug>', methods=['GET'])
@jwt_required()
def get_page(slug):
    """获取单个页面"""
    page = Page.query.filter_by(slug=slug).first()
    
    if not page:
        return jsonify({'error': 'Page not found'}), 404
    
    return jsonify(page.to_dict())


@admin_bp.route('/pages/<slug>', methods=['PUT'])
@jwt_required()
def update_page(slug):
    """更新页面内容"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    page = Page.query.filter_by(slug=slug).first()
    
    if page:
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
    else:
        page = Page(
            slug=slug,
            title=data.get('title', slug.title()),
            content=data.get('content', {})
        )
        db.session.add(page)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '页面保存成功', 'page': page.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/pages/<slug>', methods=['DELETE'])
@jwt_required()
def delete_page(slug):
    """删除页面"""
    page = Page.query.filter_by(slug=slug).first()
    
    if not page:
        return jsonify({'error': 'Page not found'}), 404
    
    try:
        db.session.delete(page)
        db.session.commit()
        return jsonify({'success': True, 'message': '页面已删除'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    """获取报名记录列表"""
    status = (request.args.get('status') or 'all').strip().lower()

    query = Application.query
    if status and status != 'all':
        query = query.filter(Application.status == status)

    applications = query.order_by(Application.created_at.desc()).all()
    return jsonify([application.to_dict() for application in applications])


@admin_bp.route('/applications/<int:application_id>', methods=['PATCH'])
@jwt_required()
def update_application(application_id):
    """更新报名记录处理状态"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404

    status = data.get('status')
    admin_note = data.get('admin_note')
    allowed_statuses = {'pending', 'reviewing', 'processed', 'archived'}

    if status is not None:
        status = str(status).strip().lower()
        if status not in allowed_statuses:
            return jsonify({'error': 'Invalid application status'}), 400
        application.status = status
        application.processed_at = None if status == 'pending' else datetime.utcnow()

    if admin_note is not None:
        application.admin_note = str(admin_note).strip() or None

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '报名记录已更新',
            'application': application.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片文件"""
    file = request.files.get('file')

    if not file or not file.filename:
        return jsonify({'error': 'No file provided'}), 400

    if not allowed_image_file(file.filename):
        return jsonify({'error': 'Unsupported image format'}), 400

    original_name = secure_filename(file.filename)
    ext = os.path.splitext(original_name)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(file_path)
        file_url = f"{request.host_url.rstrip('/')}/uploads/{filename}"
        return jsonify({
            'success': True,
            'message': '图片上传成功',
            'filename': filename,
            'url': file_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/pages/<slug>/reset', methods=['POST'])
@jwt_required()
def reset_page(slug):
    """恢复单个页面为默认内容"""
    page_default = DEFAULT_PAGES.get(slug)

    if not page_default:
        return jsonify({'error': 'No default data found for this page'}), 404

    page = Page.query.filter_by(slug=slug).first()

    if page:
        page.title = page_default['title']
        page.content = copy.deepcopy(page_default['content'])
    else:
        page = Page(
            slug=slug,
            title=page_default['title'],
            content=copy.deepcopy(page_default['content'])
        )
        db.session.add(page)

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '页面已恢复默认', 'page': page.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/reset-all', methods=['POST'])
@jwt_required()
def reset_all():
    """恢复整个站点为默认内容"""
    try:
        reset_configs_to_default()
        reset_pages_to_default()
        db.session.commit()
        return jsonify({'success': True, 'message': '所有配置和子页面已恢复默认'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/export', methods=['GET'])
@jwt_required()
def export_all():
    """导出所有配置和页面"""
    configs = SiteConfig.query.all()
    pages = Page.query.all()
    
    config_data = {}
    for config in configs:
        config_data[config.config_key] = config.config_value
    
    pages_data = {}
    for page in pages:
        pages_data[page.slug] = {
            'title': page.title,
            'content': page.content
        }
    
    return jsonify({
        'config': config_data,
        'pages': pages_data
    })


@admin_bp.route('/import', methods=['POST'])
@jwt_required()
def import_all():
    """导入配置和页面"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'config' in data:
            for key, value in data['config'].items():
                config = SiteConfig.query.filter_by(config_key=key).first()
                if config:
                    config.config_value = value
                else:
                    config = SiteConfig(config_key=key, config_value=value)
                    db.session.add(config)
        
        if 'pages' in data:
            for slug, page_data in data['pages'].items():
                page = Page.query.filter_by(slug=slug).first()
                if page:
                    page.title = page_data.get('title', page.title)
                    page.content = page_data.get('content', page.content)
                else:
                    page = Page(
                        slug=slug,
                        title=page_data.get('title', slug.title()),
                        content=page_data.get('content', {})
                    )
                    db.session.add(page)
        
        db.session.commit()
        return jsonify({'success': True, 'message': '数据导入成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
