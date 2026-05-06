"""
数据库初始化脚本
运行方式: python init_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, SiteConfig, Page, AdminUser
from defaults import DEFAULT_SITE_CONFIG, DEFAULT_PAGES


def init_database():
    """初始化数据库"""
    app = create_app()

    with app.app_context():
        print("创建数据库表...")
        db.create_all()

        existing_admin = AdminUser.query.filter_by(username='admin').first()
        if not existing_admin:
            print("创建默认管理员账号...")
            admin = AdminUser(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
        else:
            print("管理员账号已存在，跳过创建")

        existing_config = SiteConfig.query.first()
        if not existing_config:
            print("导入默认站点配置...")
            for key, value in DEFAULT_SITE_CONFIG.items():
                config = SiteConfig(config_key=key, config_value=value)
                db.session.add(config)
        else:
            print("站点配置已存在，跳过导入")

        existing_pages = Page.query.first()
        if not existing_pages:
            print("导入默认页面数据...")
            for slug, page_data in DEFAULT_PAGES.items():
                page = Page(
                    slug=slug,
                    title=page_data['title'],
                    content=page_data['content']
                )
                db.session.add(page)
        else:
            print("页面数据已存在，跳过导入")

        db.session.commit()
        print("数据库初始化完成！")
        print("\n默认管理员账号：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n请在生产环境中修改默认密码！")


if __name__ == '__main__':
    init_database()
