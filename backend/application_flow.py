import json
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError

from flask import current_app, has_request_context, request

from models import SiteConfig

STATUS_PENDING = 'pending'
STATUS_REVIEWING = 'reviewing'
STATUS_PROCESSED = 'processed'
STATUS_ARCHIVED = 'archived'

RESULT_APPROVED = 'approved'
RESULT_REJECTED = 'rejected'

ACTION_REVIEWING = 'reviewing'
ACTION_APPROVE = 'approve'
ACTION_REJECT = 'reject'
ACTION_ARCHIVE = 'archive'
ACTION_RECHECK_REJECT = 'recheck_reject'

FEISHU_API_BASE = 'https://open.feishu.cn/open-apis'
FEISHU_TOKEN_CACHE = {
    'value': '',
    'expires_at': 0
}


def _escape_html(value):
    text = '' if value is None else str(value)
    return (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )


def get_feishu_http_settings():
    try:
        timeout = float(current_app.config.get('FEISHU_HTTP_TIMEOUT') or 8)
    except (TypeError, ValueError):
        timeout = 8

    try:
        retries = int(current_app.config.get('FEISHU_HTTP_RETRIES') or 0)
    except (TypeError, ValueError):
        retries = 0

    try:
        backoff_seconds = float(current_app.config.get('FEISHU_HTTP_RETRY_BACKOFF_SECONDS') or 0.6)
    except (TypeError, ValueError):
        backoff_seconds = 0.6

    if timeout <= 0:
        timeout = 8
    if retries < 0:
        retries = 0
    if backoff_seconds < 0:
        backoff_seconds = 0

    return timeout, retries, backoff_seconds


def urlopen_with_retry(req):
    timeout, retries, backoff_seconds = get_feishu_http_settings()
    last_error = None
    for attempt in range(retries + 1):
        try:
            return urllib_request.urlopen(req, timeout=timeout)
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if isinstance(error, HTTPError) and getattr(error, 'code', 0) and error.code < 500:
                raise
            if attempt >= retries:
                raise
            time.sleep(backoff_seconds * (2 ** attempt))
    raise last_error


def stringify_urlopen_error(error):
    if isinstance(error, HTTPError):
        try:
            body = error.read().decode('utf-8', errors='replace')
        except Exception:
            body = ''
        if body:
            return f'{error}; response_body={body}'
    return str(error)


def get_feishu_system_config():
    try:
        system_config = SiteConfig.query.filter_by(config_key='system').first()
        if system_config and isinstance(system_config.config_value, dict):
            return system_config.config_value
    except Exception:
        return {}
    return {}


def get_feishu_webhook_url():
    webhook_url = (get_feishu_system_config().get('feishuWebhookUrl') or '').strip()
    if not webhook_url:
        webhook_url = (current_app.config.get('FEISHU_WEBHOOK_URL') or '').strip()

    return webhook_url


def get_feishu_app_config():
    system_config = get_feishu_system_config()
    return {
        'enabled': current_app.config.get('FEISHU_APP_ENABLED'),
        'app_id': (current_app.config.get('FEISHU_APP_ID') or '').strip(),
        'app_secret': (current_app.config.get('FEISHU_APP_SECRET') or '').strip(),
        'chat_id': (system_config.get('feishuAppChatId') or current_app.config.get('FEISHU_APP_CHAT_ID') or '').strip(),
        'verification_token': (current_app.config.get('FEISHU_APP_VERIFICATION_TOKEN') or '').strip(),
        'encrypt_key': (current_app.config.get('FEISHU_APP_ENCRYPT_KEY') or '').strip()
    }


def is_feishu_app_ready():
    config = get_feishu_app_config()
    return config['enabled'] and all([
        config['app_id'],
        config['app_secret'],
        config['chat_id']
    ])


def get_feishu_delivery_mode():
    system_config = get_feishu_system_config()
    preferred_mode = (system_config.get('feishuMode') or '').strip().lower()

    if preferred_mode == 'app' and is_feishu_app_ready():
        return 'app'
    if preferred_mode == 'webhook' and get_feishu_webhook_url():
        return 'webhook'
    if is_feishu_app_ready():
        return 'app'
    if get_feishu_webhook_url():
        return 'webhook'
    return ''


def get_action_base_url():
    configured = (current_app.config.get('APPLICATION_ACTION_BASE_URL') or '').strip()
    if configured:
        return configured.rstrip('/')

    if has_request_context():
        return request.host_url.rstrip('/')

    return ''


def build_application_action_url(application):
    base_url = get_action_base_url()
    if not base_url or not application.action_token:
        return ''
    return f'{base_url}/api/applications/actions/{application.action_token}'


def build_feishu_card_callback_url():
    base_url = get_action_base_url()
    if not base_url:
        return ''
    return f'{base_url}/api/feishu/cards/callback'


def get_tenant_access_token():
    now = int(time.time())
    if FEISHU_TOKEN_CACHE['value'] and FEISHU_TOKEN_CACHE['expires_at'] > now + 120:
        return FEISHU_TOKEN_CACHE['value'], ''

    app_config = get_feishu_app_config()
    if not app_config['app_id'] or not app_config['app_secret']:
        return '', 'FEISHU_APP_ID 或 FEISHU_APP_SECRET 未配置'

    payload = json.dumps({
        'app_id': app_config['app_id'],
        'app_secret': app_config['app_secret']
    }).encode('utf-8')
    req = urllib_request.Request(
        f'{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urlopen_with_retry(req) as response:
            response_body = json.loads(response.read().decode('utf-8') or '{}')
            if response_body.get('code') != 0:
                return '', response_body.get('msg', '获取 tenant_access_token 失败')

            FEISHU_TOKEN_CACHE['value'] = response_body.get('tenant_access_token', '')
            FEISHU_TOKEN_CACHE['expires_at'] = now + int(response_body.get('expire', 7200))
            return FEISHU_TOKEN_CACHE['value'], ''
    except (HTTPError, URLError, TimeoutError) as error:
        return '', stringify_urlopen_error(error)


def send_feishu_webhook_payload(payload):
    webhook_url = get_feishu_webhook_url()
    if not webhook_url:
        return False, 'FEISHU_WEBHOOK_URL 未配置'

    body = json.dumps(payload).encode('utf-8')
    req = urllib_request.Request(
        webhook_url,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urlopen_with_retry(req) as response:
            response_body = json.loads(response.read().decode('utf-8') or '{}')
            if response_body.get('StatusCode') == 0:
                return True, ''
            return False, response_body.get('StatusMessage', '飞书通知失败')
    except (HTTPError, URLError, TimeoutError) as error:
        return False, stringify_urlopen_error(error)


def call_feishu_open_api(path, method='POST', body=None):
    access_token, error = get_tenant_access_token()
    if error:
        return {}, error

    req = urllib_request.Request(
        f'{FEISHU_API_BASE}{path}',
        data=json.dumps(body or {}).encode('utf-8') if body is not None else None,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        },
        method=method
    )

    try:
        with urlopen_with_retry(req) as response:
            response_body = json.loads(response.read().decode('utf-8') or '{}')
            if response_body.get('code') != 0:
                return response_body, response_body.get('msg', '飞书应用调用失败')
            return response_body, ''
    except (HTTPError, URLError, TimeoutError) as error:
        return {}, stringify_urlopen_error(error)


def update_application_message_context(application, response_data, delivery_mode):
    data = response_data.get('data') or {}
    if data.get('message_id'):
        application.feishu_message_id = data.get('message_id')
    if data.get('open_message_id'):
        application.feishu_open_message_id = data.get('open_message_id')
    application.feishu_delivery_mode = delivery_mode


def build_feishu_action_button(text, action, application, button_type='default', submit=False):
    button = {
        'tag': 'button',
        'text': {
            'tag': 'plain_text',
            'content': text
        },
        'type': button_type,
        'value': {
            'action': action,
            'action_token': application.action_token
        }
    }

    if submit:
        button['action_type'] = 'request'
        callback_url = build_feishu_card_callback_url()
        if callback_url:
            button['url'] = callback_url

    return button


def build_application_card(application, title, status_label, template='blue', delivery_mode='webhook', include_actions=True):
    action_url = build_application_action_url(application)
    elements = [
        {'tag': 'markdown', 'content': f'**当前状态**：{status_label}'},
        {'tag': 'markdown', 'content': f'**报名方向**：{application.group_name}'},
        {'tag': 'markdown', 'content': f'**姓名**：{application.name}\n**学号**：{application.student_id}'},
        {'tag': 'markdown', 'content': f'**专业年级**：{application.grade_major}\n**手机号**：{application.phone}'},
        {'tag': 'markdown', 'content': f'**邮箱**：{application.email}\n**GitHub**：{application.github_url or "未填写"}'},
        {'tag': 'markdown', 'content': f'**作品集**：{application.portfolio_url or "未填写"}'},
        {'tag': 'markdown', 'content': f'**相关经历**：\n{application.experience or "未填写"}'},
        {'tag': 'markdown', 'content': f'**报名说明**：\n{application.motivation}'}
    ]

    if application.review_group_info:
        elements.append({'tag': 'markdown', 'content': f'**考核群信息**：\n{application.review_group_info}'})

    if application.admin_note:
        elements.append({'tag': 'markdown', 'content': f'**后台备注**：\n{application.admin_note}'})

    if application.last_email_type:
        email_status = '已发送' if application.last_email_sent else f'发送失败：{application.last_email_error or "未知错误"}'
        elements.append({'tag': 'markdown', 'content': f'**最近邮件**：{application.last_email_type} · {email_status}'})

    if include_actions and delivery_mode == 'app':
        elements.append({
            'tag': 'input',
            'name': 'review_group_info',
            'label': {
                'tag': 'plain_text',
                'content': '考核群信息'
            },
            'placeholder': {
                'tag': 'plain_text',
                'content': '填写群号、群链接或入群说明'
            },
            'default_value': application.review_group_info or '',
            'required': False
        })
        elements.append({
            'tag': 'input',
            'name': 'admin_note',
            'label': {
                'tag': 'plain_text',
                'content': '后台备注'
            },
            'placeholder': {
                'tag': 'plain_text',
                'content': '记录面试安排、处理说明或补充信息'
            },
            'default_value': application.admin_note or '',
            'required': False,
            'input_type': 'multiline_text'
        })
        elements.append({
            'tag': 'input',
            'name': 'result_email_links',
            'label': {
                'tag': 'plain_text',
                'content': '邮件附加链接'
            },
            'placeholder': {
                'tag': 'plain_text',
                'content': '每行一个链接，例如 https://example.com'
            },
            'default_value': application.result_email_links or '',
            'required': False,
            'input_type': 'multiline_text'
        })
        elements.append({
            'tag': 'input',
            'name': 'result_email_image_url',
            'label': {
                'tag': 'plain_text',
                'content': '邮件图片 URL'
            },
            'placeholder': {
                'tag': 'plain_text',
                'content': '例如 https://example.com/qrcode.png'
            },
            'default_value': application.result_email_image_url or '',
            'required': False
        })

        action_buttons = []
        st = application.status
        rt = application.result_type

        if st in (STATUS_PENDING, STATUS_REVIEWING):
            action_buttons.extend([
                build_feishu_action_button('标记处理中', ACTION_REVIEWING, application, submit=True),
                build_feishu_action_button('通过', ACTION_APPROVE, application, 'primary', submit=True),
                build_feishu_action_button('拒绝', ACTION_REJECT, application, 'danger', submit=True)
            ])
        elif st == STATUS_PROCESSED and rt == RESULT_APPROVED:
            action_buttons.append(
                build_feishu_action_button('归档录用', ACTION_ARCHIVE, application, 'primary', submit=True)
            )
        elif st == STATUS_ARCHIVED:
            pass
        elif st == STATUS_PROCESSED and rt == RESULT_REJECTED:
            pass

        if action_url:
            action_buttons.append({
                'tag': 'button',
                'text': {
                    'tag': 'plain_text',
                    'content': '打开处理页'
                },
                'type': 'default',
                'url': action_url
            })

        if action_buttons:
            elements.append({
                'tag': 'action',
                'actions': action_buttons
            })
    elif action_url:
        elements.append({
            'tag': 'action',
            'actions': [
                {
                    'tag': 'button',
                    'text': {
                        'tag': 'plain_text',
                        'content': '打开处理页'
                    },
                    'type': 'primary',
                    'url': action_url
                }
            ]
        })

    elements.append({
        'tag': 'note',
        'elements': [
            {'tag': 'plain_text', 'content': f'提交时间：{application.created_at.strftime("%Y-%m-%d %H:%M:%S")}'}
        ]
    })

    return {
        'config': {'wide_screen_mode': True},
        'header': {
            'title': {
                'tag': 'plain_text',
                'content': title
            },
            'template': template
        },
        'elements': elements
    }


def send_pending_application_card(application):
    delivery_mode = get_feishu_delivery_mode()
    card = build_application_card(
        application,
        f'新的报名申请 - {application.name}',
        '待处理',
        template='blue',
        delivery_mode=delivery_mode
    )

    if delivery_mode == 'app':
        app_config = get_feishu_app_config()
        response_data, error = call_feishu_open_api(
            '/im/v1/messages?receive_id_type=chat_id',
            method='POST',
            body={
                'receive_id': app_config['chat_id'],
                'msg_type': 'interactive',
                'content': json.dumps(card, ensure_ascii=False)
            }
        )
        if error:
            return False, error
        update_application_message_context(application, response_data, 'app')
        return True, ''

    if delivery_mode == 'webhook':
        application.feishu_delivery_mode = 'webhook'
        return send_feishu_webhook_payload({
            'msg_type': 'interactive',
            'card': card
        })

    return False, '未配置飞书通知方式'


def get_status_label(application):
    if application.status == STATUS_REVIEWING:
        return '处理中'
    if application.status == STATUS_PROCESSED and application.result_type == RESULT_APPROVED:
        return '已处理 · 通过'
    if application.status == STATUS_PROCESSED and application.result_type == RESULT_REJECTED:
        return '已处理 · 拒绝'
    if application.status == STATUS_ARCHIVED:
        return '已归档'
    return '待处理'


def send_status_update_card(application):
    status_label = get_status_label(application)
    delivery_mode = application.feishu_delivery_mode or get_feishu_delivery_mode()
    card = build_application_card(
        application,
        f'报名处理更新 - {application.name}',
        status_label,
        template='turquoise',
        delivery_mode=delivery_mode,
        include_actions=delivery_mode == 'app'
    )

    if delivery_mode == 'app':
        if application.feishu_message_id:
            response_data, error = call_feishu_open_api(
                f'/im/v1/messages/{application.feishu_message_id}',
                method='PATCH',
                body={
                    'msg_type': 'interactive',
                    'content': json.dumps(card, ensure_ascii=False)
                }
            )
            if not error:
                update_application_message_context(application, response_data, 'app')
                return True, ''

        response_data, error = call_feishu_open_api(
            '/im/v1/messages?receive_id_type=chat_id',
            method='POST',
            body={
                'receive_id': get_feishu_app_config()['chat_id'],
                'msg_type': 'interactive',
                'content': json.dumps(card, ensure_ascii=False)
            }
        )
        if error:
            return False, error
        update_application_message_context(application, response_data, 'app')
        return True, ''

    if delivery_mode == 'webhook':
        application.feishu_delivery_mode = 'webhook'
        return send_feishu_webhook_payload({
            'msg_type': 'interactive',
            'card': card
        })

    return False, '未配置飞书通知方式'


def is_feishu_callback_request(payload):
    header = payload.get('header') or {}
    return (
        payload.get('type') == 'url_verification' or
        payload.get('schema') == '2.0' or
        header.get('event_type', '').startswith('card.') or
        bool(payload.get('action')) or
        bool((payload.get('event') or {}).get('action'))
    )


def validate_feishu_callback(payload):
    verification_token = get_feishu_app_config().get('verification_token')
    if not verification_token:
        return True, ''

    provided = (
        (payload.get('header') or {}).get('token') or
        payload.get('token') or
        ((payload.get('event') or {}).get('token'))
    )
    if provided == verification_token:
        return True, ''
    return False, '飞书回调 token 校验失败'


def _parse_feishu_value(raw):
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def extract_feishu_callback_action(payload):
    event = payload.get('event') or payload
    action = event.get('action') or {}
    context = event.get('context') or {}
    value = _parse_feishu_value(action.get('value') or event.get('value'))
    form_value = action.get('form_value') or event.get('form_value') or {}
    if isinstance(form_value, str):
        form_value = _parse_feishu_value(form_value)

    return {
        'action': (value.get('action') or '').strip().lower(),
        'action_token': (value.get('action_token') or '').strip(),
        'review_group_info': (form_value.get('review_group_info') or '').strip(),
        'admin_note': (form_value.get('admin_note') or '').strip(),
        'result_email_links': (form_value.get('result_email_links') or '').strip(),
        'result_email_image_url': (form_value.get('result_email_image_url') or '').strip(),
        'message_id': context.get('message_id') or event.get('message_id') or '',
        'open_message_id': context.get('open_message_id') or event.get('open_message_id') or ''
    }


def build_feishu_callback_response(success, message, application=None):
    response = {
        'toast': {
            'type': 'success' if success else 'error',
            'content': message
        }
    }

    if application:
        card_body = build_application_card(
            application,
            f'报名处理更新 - {application.name}',
            get_status_label(application),
            template='turquoise',
            delivery_mode='app',
            include_actions=True
        )
        response['card'] = {
            'type': 'raw',
            'data': card_body
        }

    return response


def send_email(subject, to_email, text_content, html_content=None):
    if not current_app.config.get('MAIL_ENABLED'):
        return False, '邮件发送未启用'

    smtp_host = (current_app.config.get('SMTP_HOST') or '').strip()
    smtp_username = (current_app.config.get('SMTP_USERNAME') or '').strip()
    smtp_password = (current_app.config.get('SMTP_PASSWORD') or '').strip()
    from_email = (current_app.config.get('MAIL_FROM_EMAIL') or '').strip()

    if not smtp_host or not from_email or not to_email:
        return False, '邮件配置不完整'

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = f'{current_app.config.get("MAIL_FROM_NAME")} <{from_email}>'
    message['To'] = to_email
    message.set_content(text_content)
    if html_content:
        message.add_alternative(html_content, subtype='html')

    smtp_port = current_app.config.get('SMTP_PORT') or 587
    smtp_use_ssl = current_app.config.get('SMTP_USE_SSL')
    smtp_use_tls = current_app.config.get('SMTP_USE_TLS')

    try:
        if smtp_use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                if smtp_username:
                    server.login(smtp_username, smtp_password)
                server.send_message(message)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                if smtp_use_tls:
                    server.starttls()
                if smtp_username:
                    server.login(smtp_username, smtp_password)
                server.send_message(message)
        return True, ''
    except Exception as error:
        return False, str(error)


def build_result_email(application):
    if application.result_type == RESULT_APPROVED:
        text_lines = [
            f'{application.name} 同学，你好：',
            '',
            f'你报名的 {application.group_name} 已进入下一阶段。',
            '请加入以下考核群，并留意后续通知：',
            application.review_group_info or '考核群信息待补充',
        ]

        links_text = (application.result_email_links or '').strip()
        if links_text:
            text_lines.extend(['', '相关链接：'])
            text_lines.extend([line.strip() for line in links_text.splitlines() if line.strip()])

        image_url = (application.result_email_image_url or '').strip()
        if image_url:
            text_lines.extend(['', f'相关图片：{image_url}'])

        text_lines.extend(['', '如有问题可直接回复本邮件。', '', '星雨作坊'])
        text_content = '\n'.join(text_lines)

        html_parts = [
            f'<p>{application.name} 同学，你好：</p>',
            f'<p>你报名的 <strong>{application.group_name}</strong> 已进入下一阶段。</p>',
            '<p>请加入以下考核群，并留意后续通知：</p>',
            f'<pre style="white-space:pre-wrap;word-break:break-word;background:#f6f8fa;padding:12px;border-radius:8px">{_escape_html(application.review_group_info or "考核群信息待补充")}</pre>'
        ]

        if links_text:
            link_items = []
            for line in [l.strip() for l in links_text.splitlines() if l.strip()]:
                safe = _escape_html(line)
                if line.lower().startswith(('http://', 'https://')):
                    link_items.append(f'<li><a href="{safe}" target="_blank" rel="noreferrer">{safe}</a></li>')
                else:
                    link_items.append(f'<li>{safe}</li>')
            if link_items:
                html_parts.append('<p>相关链接：</p><ul>' + ''.join(link_items) + '</ul>')

        if image_url and image_url.lower().startswith(('http://', 'https://')):
            safe_img = _escape_html(image_url)
            html_parts.append(f'<p><img src="{safe_img}" alt="相关图片" style="max-width:100%;height:auto;border-radius:10px"/></p>')

        html_parts.append('<p>如有问题可直接回复本邮件。</p><p>星雨作坊</p>')
        html_content = ''.join(html_parts)

        return (
            '星雨作坊报名结果通知',
            text_content,
            html_content,
            'result_approved'
        )

    text_content = '\n'.join([
        f'{application.name} 同学，你好：',
        '',
        f'感谢你报名 {application.group_name}。',
        '很遗憾，本次未能进入下一阶段，但仍感谢你的关注与投入。',
        '欢迎后续继续关注星雨作坊的活动与招新信息。',
        '',
        '星雨作坊'
    ])
    html_content = ''.join([
        f'<p>{application.name} 同学，你好：</p>',
        f'<p>感谢你报名 <strong>{application.group_name}</strong>。</p>',
        '<p>很遗憾，本次未能进入下一阶段，但仍感谢你的关注与投入。</p>',
        '<p>欢迎后续继续关注星雨作坊的活动与招新信息。</p>',
        '<p>星雨作坊</p>'
    ])
    return (
        '星雨作坊报名结果通知',
        text_content,
        html_content,
        'result_rejected'
    )


def build_welcome_email(application):
    lines = [
        f'{application.name} 同学，你好：',
        '',
        f'恭喜你已完成 {application.group_name} 的录用流程，当前状态已归档。',
        '欢迎正式加入星雨作坊，后续请留意群内与邮件通知。'
    ]
    if application.review_group_info:
        lines.extend(['', '考核 / 入群信息：', application.review_group_info])
    lines.extend(['', '星雨作坊'])
    text_content = '\n'.join(lines)
    html_parts = [
        f'<p>{application.name} 同学，你好：</p>',
        f'<p>恭喜你已完成 <strong>{application.group_name}</strong> 的录用流程，当前状态已归档。</p>',
        '<p>欢迎正式加入星雨作坊，后续请留意群内与邮件通知。</p>'
    ]
    if application.review_group_info:
        html_parts.append('<p>考核 / 入群信息：</p>')
        html_parts.append(
            f'<pre style="white-space:pre-wrap;word-break:break-word;background:#f6f8fa;padding:12px;border-radius:8px">{_escape_html(application.review_group_info)}</pre>'
        )
    html_parts.append('<p>星雨作坊</p>')
    return (
        '欢迎加入星雨作坊',
        text_content,
        ''.join(html_parts),
        'welcome'
    )


def send_status_email(application, mail_kind):
    if mail_kind == 'welcome':
        subject, content, html_content, email_type = build_welcome_email(application)
    else:
        subject, content, html_content, email_type = build_result_email(application)

    sent, error = send_email(subject, application.email, content, html_content)
    application.last_email_type = email_type
    application.last_email_sent = sent
    application.last_email_error = error or None
    application.last_email_sent_at = datetime.utcnow() if sent else None
    return sent, error


def apply_application_action(application, action, payload=None):
    payload = payload or {}
    normalized_action = (action or '').strip().lower()
    review_group_info = str(payload.get('review_group_info') or '').strip()
    admin_note = payload.get('admin_note')
    result_email_links = payload.get('result_email_links')
    result_email_image_url = payload.get('result_email_image_url')

    if admin_note is not None:
        application.admin_note = str(admin_note).strip() or None

    if review_group_info:
        application.review_group_info = review_group_info

    if result_email_links is not None:
        application.result_email_links = str(result_email_links).strip() or None

    if result_email_image_url is not None:
        application.result_email_image_url = str(result_email_image_url).strip() or None

    if normalized_action == ACTION_REVIEWING:
        application.status = STATUS_REVIEWING
        application.result_type = None
        application.processed_at = datetime.utcnow()
        return '已标记为处理中', None

    if normalized_action == ACTION_APPROVE:
        if not review_group_info and not application.review_group_info:
            raise ValueError('通过时需要填写考核群信息')
        application.status = STATUS_PROCESSED
        application.result_type = RESULT_APPROVED
        application.processed_at = datetime.utcnow()
        return '已通过并准备发送结果邮件', 'result'

    if normalized_action == ACTION_REJECT:
        application.status = STATUS_PROCESSED
        application.result_type = RESULT_REJECTED
        application.processed_at = datetime.utcnow()
        return '已拒绝并准备发送结果邮件', 'result'

    if normalized_action == ACTION_RECHECK_REJECT:
        if application.status != STATUS_PROCESSED or application.result_type != RESULT_APPROVED:
            raise ValueError('仅可在「已通过」后执行二次考核未通过')
        application.status = STATUS_PROCESSED
        application.result_type = RESULT_REJECTED
        application.processed_at = datetime.utcnow()
        return '已标记为二次考核未通过并准备发送结果邮件', 'result'

    if normalized_action == ACTION_ARCHIVE:
        if application.status != STATUS_PROCESSED or application.result_type != RESULT_APPROVED:
            raise ValueError('仅可在「已通过」后执行归档录用')
        application.status = STATUS_ARCHIVED
        application.processed_at = datetime.utcnow()
        return '已归档并准备发送欢迎邮件', 'welcome'

    raise ValueError('不支持的处理动作')
