# 星雨作坊官网 CMS

星雨作坊（Xingyu Studio）是一个校园创意社团的官方展示平台，基于 **Vue 3 + Flask + MySQL** 全栈内容管理系统构建。支持可视化后台编辑、项目作品展示、报名管理、飞书通知与邮件推送。

## 功能特性

- **品牌首页**：Hero 展示、社团简介、精选项目、开源精神等区块，GSAP 动画驱动
- **作品展示**：项目画廊 + 详情页，支持截图轮播、技术栈标签、贡献成员关联
- **成员介绍**：按小组分类展示，关联参与项目
- **CMS 后台**：JWT 认证，可视化编辑器，实时预览，图片上传
- **报名系统**：在线表单提交，飞书卡片通知，审批流程，结果邮件
- **数据管理**：导入/导出备份，整站恢复默认

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3、Vite、Tailwind CSS 4、GSAP、Vue Router |
| 后端 | Flask、SQLAlchemy、Flask-JWT-Extended、PyMySQL |
| 数据库 | MySQL 8.0 |
| 部署 | Docker Compose（Nginx + Flask + MySQL） |

## 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone <repo-url>
cd base_web

# 2. 启动后端
cd backend
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env   # 编辑 .env 填写数据库配置
python init_db.py
python app.py

# 3. 启动前端（新终端）
cd base_web
npm install
npm run dev
```

访问 `http://localhost:5173`，管理后台 `http://localhost:5173/admin`



### Docker 部署

```bash
# 1. 构建前端
npm install && npm run build

# 2. 配置环境变量
cp .env.docker .env
# 编辑 .env，修改 SECRET_KEY、CORS_ORIGINS 等

# 3. 启动服务
docker-compose up -d --build
```

服务启动后访问 `http://服务器IP`，管理后台 `/admin`。

## 项目结构

```
base_web/
├── src/                        # Vue 前端源码
│   ├── views/                  # 页面组件（首页、项目、成员、管理后台等）
│   ├── components/             # 通用组件与后台编辑器
│   ├── services/api.js         # API 请求服务
│   ├── router/index.js         # 路由配置
│   └── data/defaultConfig.js   # 前端兜底配置
├── backend/                    # Flask 后端
│   ├── app.py                  # 应用入口
│   ├── models.py               # 数据库模型
│   ├── defaults.py             # 默认数据
│   ├── routes/                 # API 路由
│   └── Dockerfile              # 后端容器镜像
├── docker-compose.yml          # Docker Compose 编排
├── nginx.conf                  # Nginx 配置
└── .env.docker                 # Docker 环境变量模板
```

## 页面路由

| 路径 | 页面 |
|------|------|
| `/` | 首页 |
| `/members` | 成员介绍 |
| `/projects` | 项目展示 |
| `/project/:slug` | 项目详情 |
| `/join` | 加入我们 |
| `/blog` | 博客动态 |
| `/admin` | 管理后台 |

## 文档

详细技术文档见 [TECH_DOCS.md](./TECH_DOCS.md)。

## License

MIT
