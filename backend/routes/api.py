import secrets
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, render_template_string, request
from sqlalchemy import or_

from models import db, SiteConfig, Page, Application
from application_flow import (
    ACTION_APPROVE,
    ACTION_ARCHIVE,
    ACTION_REJECT,
    ACTION_REVIEWING,
    apply_application_action,
    build_application_action_url,
    build_feishu_callback_response,
    extract_feishu_callback_action,
    is_feishu_callback_request,
    send_pending_application_card,
    send_status_email,
    send_status_update_card,
    validate_feishu_callback
)

api_bp = Blueprint('api', __name__)

ACTION_PAGE_TEMPLATE = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>报名处理页</title>
    <style>
      body { margin: 0; font-family: Arial, sans-serif; background: #08101e; color: #eef4ff; }
      .page { max-width: 860px; margin: 0 auto; padding: 32px 20px 48px; }
      .card { background: rgba(12, 24, 42, 0.92); border: 1px solid rgba(121, 168, 255, 0.18); border-radius: 20px; padding: 24px; box-shadow: 0 16px 48px rgba(0, 0, 0, 0.25); }
      h1, h2, h3, p { margin-top: 0; }
      .status { display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 999px; background: rgba(121, 168, 255, 0.16); color: #9fc0ff; font-size: 13px; margin-bottom: 16px; }
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 20px; }
      .meta { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(121, 168, 255, 0.1); border-radius: 14px; padding: 14px; }
      .meta span { display: block; font-size: 12px; color: #91a7c7; margin-bottom: 6px; }
      .block { margin-bottom: 20px; }
      .block strong { display: block; margin-bottom: 8px; color: #9fc0ff; }
      textarea, input { width: 100%; box-sizing: border-box; border-radius: 12px; border: 1px solid rgba(121, 168, 255, 0.16); background: rgba(255, 255, 255, 0.04); color: #eef4ff; padding: 14px 16px; font-size: 14px; }
      textarea { min-height: 120px; resize: vertical; }
      .actions { display: grid; gap: 12px; }
      .action-row { display: flex; flex-wrap: wrap; gap: 12px; }
      button { border: none; border-radius: 12px; padding: 13px 18px; cursor: pointer; font-size: 14px; font-weight: 600; }
      .btn-primary { background: linear-gradient(135deg, #79a8ff, #9de4ff); color: #04101f; }
      .btn-secondary { background: rgba(255, 255, 255, 0.06); color: #eef4ff; border: 1px solid rgba(121, 168, 255, 0.16); }
      .btn-danger { background: rgba(255, 107, 107, 0.16); color: #ffd3d3; border: 1px solid rgba(255, 107, 107, 0.28); }
      .message { margin-bottom: 16px; padding: 14px 16px; border-radius: 12px; }
      .message.success { background: rgba(80, 200, 120, 0.12); border: 1px solid rgba(80, 200, 120, 0.22); color: #bff2cf; }
      .message.error { background: rgba(255, 107, 107, 0.12); border: 1px solid rgba(255, 107, 107, 0.22); color: #ffd3d3; }
      .hint { color: #91a7c7; font-size: 13px; line-height: 1.6; }
    </style>
  </head>
  <body>
    <div class="page">
      <div class="card">
        <div class="status">{{ status_label }}</div>
        <h1>{{ application.name }} · {{ application.group_name }}</h1>
        {% if message %}
          <div class="message {{ 'success' if success else 'error' }}">{{ message }}</div>
        {% endif %}
        <div class="grid">
          <div class="meta"><span>学号</span>{{ application.student_id }}</div>
          <div class="meta"><span>专业年级</span>{{ application.grade_major }}</div>
          <div class="meta"><span>手机号</span>{{ application.phone }}</div>
          <div class="meta"><span>邮箱</span>{{ application.email }}</div>
        </div>
        <div class="block">
          <strong>相关经历</strong>
          <p>{{ application.experience or '未填写' }}</p>
        </div>
        <div class="block">
          <strong>报名说明</strong>
          <p>{{ application.motivation }}</p>
        </div>
        <form method="post" class="actions">
          <div class="block">
            <strong>后台备注</strong>
            <textarea name="admin_note" placeholder="记录跟进说明、面试结果或补充信息">{{ application.admin_note or '' }}</textarea>
          </div>
          <div class="block">
            <strong>考核群信息</strong>
            <input name="review_group_info" value="{{ application.review_group_info or '' }}" placeholder="例如：QQ群号、飞书群链接、群二维码说明">
            <p class="hint">通过时会把这里的内容写入状态通知，并发送到报名者邮箱。</p>
          </div>
          <div class="block">
            <strong>邮件附加链接</strong>
            <textarea name="result_email_links" placeholder="每行一个链接，例如：https://example.com">{{ application.result_email_links or '' }}</textarea>
            <p class="hint">可填写考核资料、群二维码页面、表单等链接（会在通过邮件中展示）。</p>
          </div>
          <div class="block">
            <strong>邮件图片 URL</strong>
            <input name="result_email_image_url" value="{{ application.result_email_image_url or '' }}" placeholder="例如：https://example.com/qrcode.png">
            <p class="hint">填写图片直链后，邮件会尝试展示该图片（部分邮箱需要允许加载远程图片）。</p>
          </div>
          <div class="action-row">
            {% if application.status in ('pending', 'reviewing') %}
              <button class="btn-secondary" type="submit" name="action" value="reviewing">标记处理中</button>
              <button class="btn-primary" type="submit" name="action" value="approve">通过并发送结果邮件</button>
              <button class="btn-danger" type="submit" name="action" value="reject">拒绝并发送结果邮件</button>
            {% elif application.status == 'processed' and application.result_type == 'approved' %}
              <button class="btn-secondary" type="submit" name="action" value="archive">归档录用并发送欢迎邮件</button>
              <button class="btn-danger" type="submit" name="action" value="recheck_reject">第二次考核未通过并发送邮件</button>
            {% else %}
              <p class="hint">当前状态无需操作。</p>
            {% endif %}
          </div>
        </form>
      </div>
    </div>
  </body>
</html>
"""


def get_application_status_label(application):
    labels = {
        'pending': '待处理',
        'reviewing': '处理中',
        'processed': '已处理',
        'archived': '已归档'
    }
    label = labels.get(application.status, '待处理')
    if application.status == 'processed' and application.result_type == 'approved':
        return f'{label} · 已通过'
    if application.status == 'processed' and application.result_type == 'rejected':
        return f'{label} · 已拒绝'
    return label


def persist_application_action(application, action, payload=None, feishu_sync_mode='patch'):
    """feishu_sync_mode: patch=调用开放平台更新消息；skip=由飞书卡片 HTTP 回调响应体携带 raw 卡片更新，避免重复 PATCH。"""
    message, mail_kind = apply_application_action(application, action, payload)
    db.session.commit()

    email_error = ''
    if mail_kind:
        _, email_error = send_status_email(application, mail_kind)

    feishu_sent, feishu_error = True, ''
    if feishu_sync_mode == 'patch':
        feishu_sent, feishu_error = send_status_update_card(application)
        application.feishu_sent = feishu_sent
        application.feishu_error = feishu_error or None

    db.session.commit()
    return message, email_error, feishu_error


@api_bp.route('/config', methods=['GET'])
def get_site_config():
    """获取站点配置（首页内容）"""
    configs = SiteConfig.query.all()
    
    if not configs:
        return jsonify({'error': 'No configuration found'}), 404
    
    result = {}
    for config in configs:
        if config.config_key == 'system':
            continue
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
        ip_address=ip_address,
        action_token=secrets.token_hex(24)
    )

    db.session.add(application)
    db.session.flush()

    feishu_sent, feishu_error = send_pending_application_card(application)
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
        'message': '报名信息已提交，但飞书通知发送失败，请联系管理员检查飞书通知配置',
        'warning': application.feishu_error,
        'action_url': build_application_action_url(application)
    }), 201


@api_bp.route('/applications/actions/<action_token>', methods=['GET', 'POST'])
def application_action_page(action_token):
    application = Application.query.filter_by(action_token=action_token).first()
    if not application:
        return render_template_string(
            ACTION_PAGE_TEMPLATE,
            application=None,
            status_label='链接无效',
            message='未找到对应的报名记录',
            success=False
        ), 404

    message = ''
    success = True

    if request.method == 'POST':
        action = request.form.get('action')
        payload = {
            'admin_note': request.form.get('admin_note'),
            'review_group_info': request.form.get('review_group_info'),
            'result_email_links': request.form.get('result_email_links'),
            'result_email_image_url': request.form.get('result_email_image_url')
        }
        try:
            message, email_error, feishu_error = persist_application_action(application, action, payload)
            extra_messages = []
            if email_error:
                extra_messages.append(f'邮件发送失败：{email_error}')
            if feishu_error:
                extra_messages.append(f'飞书状态通知失败：{feishu_error}')
            if extra_messages:
                message = f'{message}；' + '；'.join(extra_messages)
        except ValueError as error:
            success = False
            message = str(error)
        except Exception as error:
            db.session.rollback()
            success = False
            message = str(error)

    return render_template_string(
        ACTION_PAGE_TEMPLATE,
        application=application,
        status_label=get_application_status_label(application),
        message=message,
        success=success
    )


@api_bp.route('/applications/actions', methods=['POST'])
def application_action_callback():
    data = request.get_json() or {}
    action_token = (data.get('action_token') or '').strip()
    action = data.get('action')

    if not action_token:
        return jsonify({'error': 'Missing action_token'}), 400

    application = Application.query.filter_by(action_token=action_token).first()
    if not application:
        return jsonify({'error': 'Application not found'}), 404

    try:
        message, email_error, feishu_error = persist_application_action(application, action, data)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 500

    response = {
        'success': True,
        'message': message,
        'application': application.to_dict()
    }

    if email_error:
        response['email_warning'] = email_error
    if feishu_error:
        response['feishu_warning'] = feishu_error

    return jsonify(response)


@api_bp.route('/feishu/cards/callback', methods=['POST'])
def feishu_card_callback():
    payload = request.get_json(silent=True) or {}

    if not is_feishu_callback_request(payload):
        return jsonify(build_feishu_callback_response(False, 'Unsupported callback payload'))

    valid, error = validate_feishu_callback(payload)
    if not valid:
        return jsonify(build_feishu_callback_response(False, error))

    if payload.get('type') == 'url_verification':
        return jsonify({'challenge': payload.get('challenge', '')})

    if payload.get('schema') == '2.0':
        event_verify = payload.get('event') or {}
        if event_verify.get('type') == 'url_verification':
            return jsonify({'challenge': event_verify.get('challenge', '')})

    action_payload = extract_feishu_callback_action(payload)
    action_token = action_payload.get('action_token')

    if not action_token:
        return jsonify(build_feishu_callback_response(False, '未识别到报名动作令牌'))

    application = Application.query.filter_by(action_token=action_token).first()
    if not application:
        return jsonify(build_feishu_callback_response(False, '未找到对应报名记录'))

    if action_payload.get('message_id'):
        application.feishu_message_id = action_payload['message_id']
    if action_payload.get('open_message_id'):
        application.feishu_open_message_id = action_payload['open_message_id']

    try:
        message, email_error, feishu_error = persist_application_action(
            application,
            action_payload.get('action'),
            action_payload,
            feishu_sync_mode='skip'
        )
    except ValueError as action_error:
        db.session.rollback()
        return jsonify(build_feishu_callback_response(False, str(action_error), application))
    except Exception as action_error:
        db.session.rollback()
        return jsonify(build_feishu_callback_response(False, str(action_error), application))

    extra_messages = []
    if email_error:
        extra_messages.append(f'邮件发送失败：{email_error}')
    if feishu_error:
        extra_messages.append(f'卡片更新失败：{feishu_error}')

    if extra_messages:
        message = f'{message}；' + '；'.join(extra_messages)

    return jsonify(build_feishu_callback_response(True, message, application))
