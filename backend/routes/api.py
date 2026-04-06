import json
from datetime import datetime, timedelta
from urllib import request as urllib_request
from urllib.error import URLError, HTTPError

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import or_

from models import db, SiteConfig, Page, Application

api_bp = Blueprint('api', __name__)


def send_feishu_application(application):
    webhook_url = ''

    try:
        system_config = SiteConfig.query.filter_by(config_key='system').first()
        if system_config and isinstance(system_config.config_value, dict):
            webhook_url = (system_config.config_value.get('feishuWebhookUrl') or '').strip()
    except Exception:
        webhook_url = ''

    if not webhook_url:
        webhook_url = (current_app.config.get('FEISHU_WEBHOOK_URL') or '').strip()

    if not webhook_url:
        return False, 'FEISHU_WEBHOOK_URL 未配置'

    payload = {
        'msg_type': 'interactive',
        'card': {
            'config': {'wide_screen_mode': True},
            'header': {
                'title': {
                    'tag': 'plain_text',
                    'content': f'新的报名申请 - {application.name}'
                },
                'template': 'blue'
            },
            'elements': [
                {'tag': 'markdown', 'content': f'**报名方向**：{application.group_name}'},
                {'tag': 'markdown', 'content': f'**姓名**：{application.name}\n**学号**：{application.student_id}'},
                {'tag': 'markdown', 'content': f'**专业年级**：{application.grade_major}\n**手机号**：{application.phone}'},
                {'tag': 'markdown', 'content': f'**邮箱**：{application.email}\n**GitHub**：{application.github_url or "未填写"}'},
                {'tag': 'markdown', 'content': f'**作品集**：{application.portfolio_url or "未填写"}'},
                {'tag': 'markdown', 'content': f'**相关经历**：\n{application.experience or "未填写"}'},
                {'tag': 'markdown', 'content': f'**报名说明**：\n{application.motivation}'},
                {'tag': 'note', 'elements': [
                    {'tag': 'plain_text', 'content': f'提交时间：{application.created_at.strftime("%Y-%m-%d %H:%M:%S")}'}
                ]}
            ]
        }
    }

    body = json.dumps(payload).encode('utf-8')
    req = urllib_request.Request(
        webhook_url,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib_request.urlopen(req, timeout=8) as response:
            response_body = json.loads(response.read().decode('utf-8') or '{}')
            if response_body.get('StatusCode') == 0:
                return True, ''
            return False, response_body.get('StatusMessage', '飞书通知失败')
    except (HTTPError, URLError, TimeoutError) as error:
        return False, str(error)


@api_bp.route('/config', methods=['GET'])
def get_site_config():
    """获取站点配置（首页内容）"""
    configs = SiteConfig.query.all()
    
    if not configs:
        return jsonify({'error': 'No configuration found'}), 404
    
    result = {}
    for config in configs:
        result[config.config_key] = config.config_value
    
    return jsonify(result)


@api_bp.route('/pages', methods=['GET'])
def get_all_pages():
    """获取所有页面列表（仅基本信息）"""
    pages = Page.query.all()
    return jsonify([{
        'slug': p.slug,
        'title': p.title,
        'updated_at': p.updated_at.isoformat() if p.updated_at else None
    } for p in pages])


@api_bp.route('/pages/<slug>', methods=['GET'])
def get_page(slug):
    """获取单个页面内容"""
    page = Page.query.filter_by(slug=slug).first()
    
    if not page:
        return jsonify({'error': 'Page not found'}), 404
    
    return jsonify(page.to_dict())


@api_bp.route('/applications', methods=['POST'])
def submit_application():
    """提交报名表"""
    data = request.get_json()

    required_fields = ['name', 'student_id', 'grade_major', 'phone', 'email', 'group_id', 'group_name', 'motivation']
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address:
        ip_address = ip_address.split(',')[0].strip()

    cooldown_minutes = current_app.config.get('APPLICATION_RATE_LIMIT_MINUTES', 10)
    cooldown_time = datetime.utcnow() - timedelta(minutes=cooldown_minutes)

    existing_application = Application.query.filter(
        Application.created_at >= cooldown_time,
        or_(
            Application.ip_address == ip_address,
            Application.email == data.get('email'),
            Application.phone == data.get('phone')
        )
    ).order_by(Application.created_at.desc()).first()

    if existing_application:
        return jsonify({'error': f'短时间内请勿重复报名，请 {cooldown_minutes} 分钟后再试'}), 429

    github_url = (data.get('github_url') or '').strip()
    if github_url == 'https://github.com':
        github_url = ''

    application = Application(
        name=data.get('name', '').strip(),
        student_id=data.get('student_id', '').strip(),
        grade_major=data.get('grade_major', '').strip(),
        phone=data.get('phone', '').strip(),
        email=data.get('email', '').strip(),
        group_id=data.get('group_id', '').strip(),
        group_name=data.get('group_name', '').strip(),
        github_url=github_url or None,
        portfolio_url=(data.get('portfolio_url') or '').strip() or None,
        experience=(data.get('experience') or '').strip() or None,
        motivation=data.get('motivation', '').strip(),
        ip_address=ip_address
    )

    db.session.add(application)
    db.session.flush()

    feishu_sent, feishu_error = send_feishu_application(application)
    application.feishu_sent = feishu_sent
    application.feishu_error = feishu_error or None

    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 500

    if feishu_sent:
        return jsonify({'success': True, 'message': '报名信息已提交，处理人将尽快查看'}), 201

    return jsonify({
        'success': True,
        'message': '报名信息已提交，但飞书通知发送失败，请联系管理员检查 webhook 配置',
        'warning': application.feishu_error
    }), 201
