# 星雨作坊 CMS 后端

基于 Flask + MySQL 的内容管理系统后端。

## 环境要求

- Python 3.9+
- MySQL 5.7+

## 安装步骤

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

1. 创建 MySQL 数据库：

```sql
CREATE DATABASE xingyu_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 复制环境变量配置文件：

```bash
cp .env.example .env
```

3. 编辑 `.env` 文件，填入你的 MySQL 配置。

### 4. 初始化数据库

```bash
python init_db.py
```

这将创建数据表并导入默认数据，包括：
- 默认管理员账号 (admin / admin123)
- 默认站点配置
- 默认页面内容

### 5. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API 接口

### 公开接口

| 方法 | 路径 | 说明 |
|-----|------|-----|
| GET | /api/config | 获取站点配置 |
| GET | /api/pages | 获取所有页面列表 |
| GET | /api/pages/:slug | 获取单个页面内容 |
| GET | /health | 健康检查 |

### 管理接口（需要 JWT 认证）

| 方法 | 路径 | 说明 |
|-----|------|-----|
| POST | /api/admin/login | 管理员登录 |
| GET | /api/admin/me | 获取当前用户信息 |
| GET | /api/admin/config | 获取站点配置 |
| PUT | /api/admin/config | 更新站点配置 |
| GET | /api/admin/pages | 获取所有页面 |
| GET | /api/admin/pages/:slug | 获取单个页面 |
| PUT | /api/admin/pages/:slug | 更新页面 |
| DELETE | /api/admin/pages/:slug | 删除页面 |
| GET | /api/admin/export | 导出所有数据 |
| POST | /api/admin/import | 导入数据 |

### 认证方式

登录成功后会返回 JWT token，在后续请求中添加 Header：

```
Authorization: Bearer <token>
```

## 生产部署

建议使用 Gunicorn + Nginx 部署：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

或使用 Docker（需自行编写 Dockerfile）。
