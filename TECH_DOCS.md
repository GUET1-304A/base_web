# 星雨作坊官网技术开发文档 v3.1

## 目录

1. [快速启动（怎么跑起来）](#快速启动怎么跑起来)
2. [项目概述](#项目概述)
3. [系统架构](#系统架构)
4. [技术栈](#技术栈)
5. [项目结构](#项目结构)
6. [环境配置与运行](#环境配置与运行)
7. [后端 API 服务](#后端-api-服务)
8. [报名、飞书与邮件](#报名飞书与邮件)
9. [核心模块详解](#核心模块详解)
10. [路由系统](#路由系统)
11. [组件架构](#组件架构)
12. [状态管理](#状态管理)
13. [动画系统](#动画系统)
14. [样式方案](#样式方案)
15. [数据配置](#数据配置)
16. [后台管理系统](#后台管理系统)
17. [前端 API 服务（api.js）](#前端-api-服务apijs)
18. [Vue 子页面](#vue-子页面)
19. [开发指南](#开发指南)
20. [部署说明](#部署说明)
21. [版本记录](#版本记录)
22. [文档信息](#文档信息)

---

## 快速启动（怎么跑起来）

按顺序完成以下步骤即可在本地同时跑起 **前端（Vite）** 与 **后端（Flask）**。默认前端 `http://localhost:5173`，后端 `http://localhost:5000`。

### 1. 准备环境


| 依赖      | 建议版本              |
| ------- | ----------------- |
| Node.js | ≥ 18              |
| npm     | ≥ 9               |
| Python  | ≥ 3.9             |
| MySQL   | ≥ 5.7，字符集 utf8mb4 |


### 2. 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE xingyu_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置并启动后端

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows；Unix 使用: cp .env.example .env
```

编辑 `backend/.env`：至少填写 **MYSQL_***、**JWT_SECRET_KEY**、**SECRET_KEY**。可选：飞书、邮件、**CORS_ORIGINS**（需包含前端地址，默认已含 `http://localhost:5173`）。

初始化表与默认数据（管理员、首页配置、子页面等）：

```bash
python init_db.py
```

启动 API（监听 `APP_HOST`:`APP_PORT`，默认 `0.0.0.0:5000`）：

```bash
python app.py
```

自检：浏览器或 curl 访问 `http://localhost:5000/health`，应返回 JSON `status: ok`。

### 4. 配置并启动前端

在项目根目录（与 `package.json` 同级）：

```bash
copy .env.example .env   # 或 cp .env.example .env
```

编辑根目录 `.env`，保证：

```env
VITE_API_BASE=http://localhost:5000/api
```

安装依赖并启动开发服务器：

```bash
npm install
npm run dev
```

### 5. 访问地址与默认账号


| 用途        | 地址                                                           |
| --------- | ------------------------------------------------------------ |
| 官网前台      | [http://localhost:5173/](http://localhost:5173/)             |
| 管理后台      | [http://localhost:5173/admin](http://localhost:5173/admin)   |
| 后端 API 前缀 | [http://localhost:5000/api](http://localhost:5000/api)       |
| 健康检查      | [http://localhost:5000/health](http://localhost:5000/health) |


默认管理员（请在生产环境修改密码）：

- 用户名：`admin`
- 密码：`admin123`

### 6. 生产构建（仅前端静态资源）

```bash
npm run build
```

产物在 `dist/`，需配合 **反向代理** 将 `/api` 指到 Flask，或由 Flask 托管 `dist`（见 [部署说明](#部署说明)）。

### 7. 常见问题


| 现象               | 排查                                                    |
| ---------------- | ----------------------------------------------------- |
| 前台一直用默认文案、后台保存无效 | 确认后端已启动，且 `VITE_API_BASE` 与浏览器能访问的 API 一致             |
| 浏览器控制台 CORS 错误   | 在 `backend/.env` 的 `CORS_ORIGINS` 中加入前端完整 origin（含端口） |
| 数据库连接失败          | 检查 MySQL 服务、`MYSQL_HOST` 等配置、数据库是否已创建                 |
| 报名飞书无反应          | 检查后台「系统设置」与 `.env` 中飞书相关项；应用机器人需公网 HTTPS 回调（见下文）      |


---

## 项目概述

星雨作坊官网是一个基于 **Vue 3 + Vite** 与 **Flask + MySQL** 的全栈内容管理系统，作为校园创意社团的官方展示平台。前后端分离：前台与后台页面由 Vue 路由承载，**业务数据以 MySQL 为准**；前端通过 `VITE_API_BASE` 访问 REST API。

### 主要功能

- **品牌首页**：Hero、社团简介、成员、产品、开源精神等区块，数据来自 `GET /api/config`
- **动画与动效**：GSAP（含 ScrollTrigger）；Lenis 仍在依赖中，可按页面选用
- **产品轮播**：多 Tab + 幻灯片展示项目
- **CMS 后台**：JWT 登录；首页各区块编辑器；**子页面** CRUD、单页恢复默认、**未保存预览**（sessionStorage）
- **系统设置**：飞书通知方式（Webhook / 应用机器人）、Webhook 地址、群 Chat ID；展示卡片回调 URL 说明
- **图片上传**：管理端上传至后端 `uploads/`，前台展示图片 URL
- **动态子页面**：多条 Vue 路由页面（关于、成员、项目、博客、加入、招新等），内容来自 `GET /api/pages/:slug`
- **加入我们 / 报名**：表单提交 `POST /api/applications`，限流；可选飞书通知与 **SMTP 结果邮件**；**报名记录**在后台列表查看与处理（与飞书卡片流程同步）
- **数据持久化**：MySQL；支持 JSON **导入/导出**与 **整站恢复默认**（后端默认值见 `backend/defaults.py`）

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户端                                   │
│  ┌─────────────────┐              ┌─────────────────────────┐   │
│  │   官网前台      │              │     管理后台            │   │
│  │  (HomeView)     │              │    (AdminView)          │   │
│  │                 │              │                         │   │
│  │  - Hero展示     │              │  - 可视化编辑器         │   │
│  │  - 社团简介     │   ←─ 数据 ─→ │  - 内容管理             │   │
│  │  - 成员介绍     │              │  - 产品管理             │   │
│  │  - 产品展示     │              │  - 实时预览             │   │
│  │  - 开源精神     │              │  - 配置导入/导出        │   │
│  └─────────────────┘              └─────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask API（/api）                             │
│  公开：config、pages、applications（POST）                        │
│  管理：/api/admin/*（JWT）、上传、导入导出、报名列表                  │
│  回调：/api/feishu/cards/callback（飞书卡片）                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MySQL（xingyu_cms）                           │
│  site_config、pages、applications、admin_users                   │
└─────────────────────────────────────────────────────────────────┘
```

### 数据流向（编辑场景）

```
AdminView / PagesEditor
        │
        ▼
  api.js（Bearer JWT）
        │
        ▼
  PUT /api/admin/config 或 PUT /api/admin/pages/:slug
        │
        ▼
  MySQL 持久化
        │
        ▼
  官网前台下次 getSiteConfig / getPage 即读到新数据
```

**预览（未保存）**：后台将当前编辑态写入 `sessionStorage`，前台带 `?previewSite=1` 或 `?previewPage=<slug>` 时 `api.js` 优先读预览数据。

---

## 技术栈

### 前端


| 类别         | 技术选型                   | 版本      | 用途              |
| ---------- | ---------------------- | ------- | --------------- |
| **框架**     | Vue 3                  | ^3.5.30 | 前端核心框架          |
| **路由**     | Vue Router             | ^5.0.4  | SPA 路由管理        |
| **构建工具**   | Vite                   | ^8.0.1  | 开发构建工具          |
| **CSS 框架** | Tailwind CSS           | ^4.2.2  | 原子化 CSS         |
| **动画库**    | GSAP (含 ScrollTrigger) | ^3.14.2 | 高性能动画           |
| **平滑滚动**   | Lenis                  | ^1.3.21 | 可选；部分页面曾用，可按需接入 |
| **语言**     | JavaScript (ES Module) | -       | 主开发语言           |


### 后端


| 类别      | 技术选型               | 版本    | 用途            |
| ------- | ------------------ | ----- | ------------- |
| **框架**  | Flask              | 3.0.0 | Python Web 框架 |
| **ORM** | Flask-SQLAlchemy   | 3.1.1 | 数据库 ORM       |
| **认证**  | Flask-JWT-Extended | 4.6.0 | JWT 认证        |
| **跨域**  | Flask-CORS         | 4.0.0 | CORS 支持       |
| **数据库** | MySQL + PyMySQL    | 1.1.0 | 数据持久化         |
| **语言**  | Python             | 3.9+  | 后端开发语言        |


### 依赖说明

```json
{
  "dependencies": {
    "gsap": "^3.14.2",
    "lenis": "^1.3.21",
    "vue": "^3.5.30",
    "vue-router": "^5.0.4"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.2.2",
    "@vitejs/plugin-vue": "^6.0.5",
    "autoprefixer": "^10.4.27",
    "postcss": "^8.5.8",
    "tailwindcss": "^4.2.2",
    "vite": "^8.0.1"
  }
}
```

---

## 项目结构

```
base_web/
├── index.html
├── package.json
├── vite.config.js
├── .env.example               # VITE_API_BASE、默认 GitHub 等
├── TECH_DOCS.md
│
├── backend/
│   ├── app.py                 # create_app、健康检查、/uploads 静态、启动
│   ├── config.py              # 环境变量与类 Config
│   ├── models.py              # SiteConfig、Page、Application、AdminUser
│   ├── defaults.py            # 默认首页配置与子页面内容（重置/初始化引用）
│   ├── application_flow.py    # 报名业务、飞书卡片/回调、SMTP
│   ├── init_db.py             # 建表并灌入初始数据（首次部署执行）
│   ├── requirements.txt
│   ├── .env.example
│   ├── uploads/               # 上传图片存储（运行时可写）
│   └── routes/
│       ├── api.py             # 公开 API、报名、飞书回调、处理页
│       └── admin.py           # 管理 API、报名列表、上传、重置
│
├── public/
│   └── pages/                 # 可选：旧路径 HTML 重定向到 Vue 路由
│
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── style.css
│   ├── constants/
│   │   └── externalLinks.js   # 前台默认外链（如 GitHub）
│   ├── router/index.js
│   ├── views/                 # Home、Admin、各子页、Join（含报名表单）
│   ├── components/
│   │   ├── Navbar.vue、Footer.vue、SkyEffects.vue
│   │   └── admin/             # 各区块编辑器、PagesEditor、SystemEditor、
│   │                          # ApplicationsManager、ImageUploadField、pages/*
│   ├── composables/           # Lenis / GSAP 等
│   ├── services/api.js        # fetch + JWT + 预览读写 sessionStorage
│   └── data/defaultConfig.js  # API 失败时的前端兜底配置
└── dist/                      # npm run build 输出
```

---

## 环境配置与运行

**一键步骤汇总见上文 [快速启动（怎么跑起来）](#快速启动怎么跑起来)。** 本节补充环境变量与运行细节。

### 后端主要环境变量（`backend/.env`）


| 变量                                                       | 说明                                 |
| -------------------------------------------------------- | ---------------------------------- |
| `MYSQL_HOST` / `PORT` / `USER` / `PASSWORD` / `DATABASE` | MySQL 连接                           |
| `SECRET_KEY` / `JWT_SECRET_KEY`                          | Flask 与 JWT，生产务必更换                 |
| `CORS_ORIGINS`                                           | 逗号分隔的前端 origin，须包含实际访问地址           |
| `UPLOAD_FOLDER`                                          | 上传目录，默认可为 `backend/uploads`        |
| `APPLICATION_RATE_LIMIT_MINUTES`                         | 报名同一 IP/邮箱/手机号的冷却时间                |
| `FEISHU_WEBHOOK_URL`                                     | Webhook 机器人地址（与后台「系统设置」可二选一或并存）    |
| `FEISHU_APP_ENABLED`                                     | 是否启用应用机器人相关能力                      |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET`                    | 飞书应用凭证                             |
| `FEISHU_APP_CHAT_ID`                                     | 接收报名卡片的群 `oc_xxx`（也可在后台 system 配置） |
| `FEISHU_APP_VERIFICATION_TOKEN`                          | 事件/卡片回调校验                          |
| `APPLICATION_ACTION_BASE_URL`                            | 报名「打开处理页」链接的站点根 URL（公网）            |
| `MAIL_ENABLED` 与 `SMTP_`* / `SMTP_FROM`                  | 报名结果邮件与欢迎邮件                        |


完整模板见 `backend/.env.example`。

### 前端环境变量（项目根 `.env`）


| 变量                                    | 说明                                              |
| ------------------------------------- | ----------------------------------------------- |
| `VITE_API_BASE`                       | 浏览器访问后端的 API 根路径，默认 `http://localhost:5000/api` |
| `VITE_DEFAULT_GITHUB_URL`             | 可选；前台部分链接兜底（以后台配置为准）                            |
| `VITE_DEFAULT_APPLICATION_GITHUB_URL` | 报名表 GitHub 占位默认                                 |


### 应用启动行为说明

- 后端 `create_app()` 会执行 `db.create_all()`，并对 `applications` 表做**轻量列迁移**（缺列则 `ALTER`），缺 `action_token` 的旧记录会补 token。
- 首次部署或空库：**必须**执行一次 `python init_db.py`。
- 开发时典型组合：终端 1 `backend` 里 `python app.py`，终端 2 项目根目录 `npm run dev`。

### 生产构建

```bash
npm run build
```

输出目录为 `dist/`。生产环境需部署静态文件 + 反向代理 API，见 [部署说明](#部署说明)。

---

## 后端 API 服务

### 数据库模型（`models.py`）

- **SiteConfig**：`config_key`（如 `hero`、`about`、`system`）+ `config_value`（JSON）。公开接口 `GET /api/config` **不返回** `system`，避免把 Webhook 等配置暴露给匿名用户；`GET /api/admin/config` 返回全部。
- **Page**：`slug`、`title`、`content`（JSON）。
- **Application**：报名表全文段；`status`、`result_type`、`review_group_info`、`admin_note`、`action_token`；飞书 `message_id` / `delivery_mode`；邮件 `last_email_*` 等。
- **AdminUser**：管理员与密码哈希。

### API 端点

**公开接口（无需认证）**


| 方法       | 路径                                  | 说明                  |
| -------- | ----------------------------------- | ------------------- |
| GET      | `/api/config`                       | 首页站点配置（不含 `system`） |
| GET      | `/api/pages`                        | 页面列表                |
| GET      | `/api/pages/<slug>`                 | 单页内容                |
| POST     | `/api/applications`                 | 提交报名（限流）            |
| GET/POST | `/api/applications/actions/<token>` | 报名处理页（HTML）         |
| POST     | `/api/applications/actions`         | JSON 触发处理（可选）       |
| POST     | `/api/feishu/cards/callback`        | 飞书卡片回调              |
| GET      | `/health`                           | 健康检查                |
| GET      | `/uploads/<path>`                   | 上传文件                |


**管理接口（JWT）**


| 方法             | 路径                              | 说明              |
| -------------- | ------------------------------- | --------------- |
| POST           | `/api/admin/login`              | 登录              |
| GET            | `/api/admin/me`                 | 当前用户            |
| GET/PUT        | `/api/admin/config`             | 读/写配置           |
| PUT            | `/api/admin/config/<key>`       | 单项更新            |
| GET/POST       | `/api/admin/pages`              | 列表/新建           |
| GET/PUT/DELETE | `/api/admin/pages/<slug>`       | 读/写/删           |
| POST           | `/api/admin/pages/<slug>/reset` | 单页恢复默认          |
| POST           | `/api/admin/reset-all`          | 全站默认            |
| GET            | `/api/admin/applications`       | 报名列表            |
| PATCH          | `/api/admin/applications/<id>`  | 更新或 `action` 流程 |
| POST           | `/api/admin/upload-image`       | 图片上传            |
| GET/POST       | `/api/admin/export` / `import`  | 备份              |


### JWT 认证

登录返回 `token`，请求头：`Authorization: Bearer <token>`。详见 `src/services/api.js`（401/422 清 token 并刷新）。

---

## 报名、飞书与邮件

逻辑见 `backend/application_flow.py`。

1. **提交报名** → 库内 **待处理** → 飞书卡片（Webhook 或应用机器人，由 `system.feishuMode` 与 `.env` 决定）。
2. **飞书按钮**：处理中 → 通过（需考核群）/拒绝 → **已处理** + 结果邮件；**已通过** 后可 **归档录用** → **已归档** + 欢迎邮件。
3. 卡片回调响应使用 `**card.type = raw`** 刷新同一张卡片；回调路径内不再重复 PATCH，避免飞书更新次数限制。
4. 后台 **报名记录** 与飞书状态对齐，支持定时静默刷新。

**开放平台**：订阅 `card.action.trigger`，URL `https://<域名>/api/feishu/cards/callback`；配置 `FEISHU_APP_VERIFICATION_TOKEN`、`APPLICATION_ACTION_BASE_URL`（公网）。

---

## 核心模块详解

### 应用入口 (main.js)

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

createApp(App).use(router).mount('#app')
```

### 根组件 (App.vue)

```vue
<template>
  <SkyEffects />
  <router-view />
</template>
```

- 全局背景效果层 `SkyEffects`
- 路由视图出口 `router-view`

### Vite 配置 (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
})
```

---

## 路由系统

### 路由配置


| 路径                 | 名称            | 组件        | 说明          |
| ------------------ | ------------- | --------- | ----------- |
| `/`                | home          | HomeView  | 首页（同步导入）    |
| `/index.html`      | -             | 重定向 → `/` | 兼容性处理       |
| `/admin`           | admin         | AdminView | 后台管理主页（懒加载） |
| `/admin/:section`  | admin-section | AdminView | 后台管理分区      |
| `/:pathMatch(.*)*` | -             | 重定向 → `/` | 404 回退      |


### 滚动行为

```javascript
scrollBehavior(to, from, savedPosition) {
  if (to.hash) {
    return {
      el: to.hash,
      top: 96,        // 顶部偏移（导航栏高度）
      behavior: 'smooth',
    }
  }
  return { top: 0 }
}
```

### 锚点导航

首页支持锚点跳转：

- `#home` - Hero 区域
- `#about` - 社团简介
- `#members` - 人员介绍
- `#products` - 产品展示
- `#open-source` - 开源精神
- `#join` - 加入我们

---

## 组件架构

### 布局组件

#### Navbar.vue - 导航栏

```vue
<template>
  <header class="topbar">
    <RouterLink class="brand" :to="{ name: 'home', hash: '#home' }">
      <span class="brand-mark">XY</span>
      <span class="brand-text">星雨作坊</span>
    </RouterLink>
    <nav class="nav">
      <RouterLink :to="{ name: 'home', hash: '#about' }">社团简介</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#members' }">人员介绍</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#products' }">产品展示</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#open-source' }">开源精神</RouterLink>
    </nav>
    <RouterLink class="nav-cta" to="/join">加入我们</RouterLink>
  </header>
</template>
```

#### Footer.vue - 页脚

```vue
<template>
  <footer class="footer">
    <p>星雨作坊 Xingyu Studio</p>
    <p>以协作连接灵感，以开源延续成长。</p>
  </footer>
</template>
```

### 效果组件

#### SkyEffects.vue - 星空背景

动态生成流星效果：

```javascript
onMounted(() => {
  const meteorCount = window.innerWidth < 760 ? 10 : 18;
  for (let index = 0; index < meteorCount; index += 1) {
    const meteor = document.createElement("span");
    meteor.className = "shooting-star";
    meteor.style.setProperty("--left", `${55 + Math.random() * 45}%`);
    meteor.style.setProperty("--top", `${-15 + Math.random() * 35}%`);
    meteor.style.setProperty("--delay", `${Math.random() * 8}s`);
    meteor.style.setProperty("--duration", `${3.8 + Math.random() * 3.2}s`);
    meteorShower.value.appendChild(meteor);
  }
});
```

---

## 状态管理

项目采用 **组件局部状态 + 服务层持久化** 的轻量级方案，未使用 Pinia/Vuex。

### 首页状态

```javascript
// HomeView.vue
const siteConfig = ref(defaultSiteConfig)      // 站点配置
const activeProductSlide = ref(0)              // 当前产品轮播索引

// 初始化加载配置
api.getSiteConfig().then((config) => {
  if (config) siteConfig.value = config
})
```

### 管理页状态

```javascript
// AdminView.vue
const siteConfig = ref(null)           // 站点配置对象
const activeSection = ref('hero')      // 当前编辑区块
const isDirty = ref(false)             // 是否有未保存更改
const message = ref('')                // 操作消息
```

---

## 动画系统

### Composables 组合式函数

#### useLenis.js - 平滑滚动

```javascript
export function useLenis() {
  let lenisInstance = null

  onMounted(() => {
    // 尊重用户偏好设置
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return

    lenisInstance = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })

    // 与 GSAP ScrollTrigger 集成
    gsap.registerPlugin(ScrollTrigger)
    lenisInstance.on("scroll", ScrollTrigger.update)
    gsap.ticker.add((time) => lenisInstance.raf(time * 1000))
  })

  onUnmounted(() => {
    if (lenisInstance) lenisInstance.destroy()
  })
}
```

#### useGsapAnimations.js - GSAP 动画

主要功能：

1. **导航高亮（ScrollSpy）**：滚动时自动高亮当前区块对应的导航项
2. **Hero 入场动画**：文字和视觉元素的渐入效果
3. **Hero 滚动视差**：随滚动产生的 3D 变换效果
4. **区块翻页动画**：`[data-reveal-section]` 标记的区块进入视口时的翻页效果

```javascript
// Hero 入场动画示例
gsap.from(heroChildren, {
  opacity: 0,
  y: 56,
  rotateX: 8,
  duration: 1.05,
  stagger: 0.09,
  ease: "power3.out",
  delay: 0.12,
})
```

#### useScrollMotion.js - 滚动状态

管理 CSS 自定义属性用于滚动驱动效果：

```javascript
// 更新 CSS 变量
root.style.setProperty("--hero-progress", heroProgressVal)
section.style.setProperty("--section-progress", progress)

// 状态类切换
section.classList.toggle("is-active-section", isActive)
section.classList.toggle("is-dimmed", isDimmed)
```

---

## 样式方案

### 全局样式 (style.css)

```css
@import "tailwindcss";
```

采用 Tailwind CSS 4 + 自定义 CSS 变量的混合方案。

### CSS 变量

```css
:root {
  --bg: #07111f;
  --bg-soft: rgba(12, 25, 45, 0.78);
  --panel: rgba(12, 24, 42, 0.78);
  --panel-border: rgba(158, 191, 255, 0.15);
  --text: #edf4ff;
  --muted: #9fb0cd;
  --primary: #79a8ff;
  --primary-strong: #95e4ff;
  --accent: #ad8cff;
}
```

### 主要样式类


| 类名                  | 用途      |
| ------------------- | ------- |
| `.site-shell`       | 页面容器    |
| `.topbar`           | 顶部导航栏   |
| `.hero`             | Hero 区域 |
| `.section`          | 通用区块    |
| `.flip-section`     | 翻页动画区块  |
| `.panel`            | 卡片面板    |
| `.flip-card`        | 翻页卡片    |
| `.button`           | 按钮基础样式  |
| `.button-primary`   | 主要按钮    |
| `.button-secondary` | 次要按钮    |


### 动画关键帧

```css
@keyframes meteor {
  0% { transform: translate(0, 0); opacity: 1; }
  100% { transform: translate(-200px, 200px); opacity: 0; }
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
```

### 响应式断点

```css
@media (max-width: 760px) { /* 移动端适配 */ }
@media (prefers-reduced-motion: reduce) { /* 减少动画 */ }
```

---

## 数据配置

### 完整配置结构 (defaultConfig.js)

```javascript
export const defaultSiteConfig = {
  // Hero 区域配置
  hero: {
    eyebrow: 'XINGYU STUDIO',
    title: '把灵感变成作品，把热爱做成长期主义。',
    description: '星雨作坊是一个面向产品、设计与技术协作的校园创意社团...',
    stats: [
      { value: '4', label: '核心方向' },
      { value: '12+', label: '协作项目' },
      { value: '100%', label: '鼓励开源' },
      { value: '5+', label: '参与开源社区' },
      { value: 'TRAE', label: '合作社区' },
      { value: 'NULL', label: '参与比赛' }
    ],
    signalCard: {
      eyebrow: '协作 · 创造 · 分享',
      title: '从 0 到 1',
      description: '产品策划 / 设计实现 / 持续开源'
    }
  },

  // 社团简介配置
  about: {
    title: '社团简介',
    description: '我们相信真正有生命力的社团...',
    items: [
      {
        title: '我们在做什么',
        description: '星雨作坊围绕产品构思、视觉设计...'
      },
      {
        title: '我们适合谁',
        description: '适合热爱互联网、愿意表达...'
      },
      {
        title: '我们的目标',
        description: '做出被同学真实使用的产品...'
      }
    ]
  },

  // 成员介绍配置
  members: {
    title: '人员介绍',
    description: '我们鼓励跨方向协作...',
    groups: [
      {
        tag: '产品策划',
        name: '流光组',
        description: '负责需求洞察、功能设计...'
      },
      {
        tag: '视觉设计',
        name: '星绘组',
        description: '负责品牌视觉、界面设计...'
      },
      {
        tag: '技术开发',
        name: '逐云组',
        description: '负责前端、后端与部署实现...'
      },
      {
        tag: '内容传播',
        name: '回声组',
        description: '负责活动记录、产品推广...'
      }
    ]
  },

  // 产品展示配置
  products: {
    title: '产品展示',
    description: '以下内容为官网展示模板...',
    categories: ['精选总览', '网站平台', '效率工具', '品牌内容'],
    slides: [
      {
        tag: '精选总览',
        title: '从灵感、工具到传播，形成完整作品链路',
        description: '星雨作坊的产品并不是孤立存在的单点项目...',
        metrics: [
          { value: '03', label: '核心章节' },
          { value: '06', label: '示例作品' },
          { value: '∞', label: '持续迭代' }
        ],
        projects: [
          {
            category: '网站平台',
            name: '星图导航',
            description: '为新成员与访客整理社团资讯...',
            link: '/onboarding',
            coverClass: 'aurora'
          }
          // ... 更多项目
        ]
      }
      // ... 更多 slides
    ]
  },

  // 开源精神配置
  openSource: {
    title: '开源精神',
    description: '对星雨作坊来说，开源不只是把代码放出来...',
    items: [
      {
        title: '共享知识',
        description: '把文档、教程、设计稿和项目复盘留下来...'
      },
      {
        title: '鼓励协作',
        description: '欢迎成员互相 review、共同维护项目...'
      },
      {
        title: '持续迭代',
        description: '开源意味着作品不是一次性交付...'
      }
    ],
    joinBanner: {
      eyebrow: 'JOIN US',
      title: '如果你也相信"做作品比只谈想法更重要"，欢迎加入星雨作坊。'
    }
  },

  // 页脚配置
  footer: {
    brand: '星雨作坊 Xingyu Studio',
    slogan: '以协作连接灵感，以开源延续成长。'
  }
}
```

---

## 后台管理系统

### 功能概述

管理后台提供可视化界面，用于编辑官网的所有内容配置。

### 访问方式

- **URL**: `/admin`
- **路由名称**: `admin`

### 界面布局

```
┌──────────────────────────────────────────────────────────────┐
│  AdminHeader：标题、未保存标记、预览、保存、当前用户            │
├─────────┬────────────────────────────────────────────────────┤
│ Sidebar │  主内容区：对应 *Editor / PagesEditor /              │
│ 首页区块 │  ApplicationsManager / SystemEditor                 │
│ 子页面   │  预览为弹窗 iframe（带 preview 查询参数）            │
│ 报名记录 │                                                    │
│ 系统设置 │                                                    │
│ 导出导入 │                                                    │
│ 恢复默认 │                                                    │
└─────────┴────────────────────────────────────────────────────┘
```

### 编辑器组件

#### HeroEditor - Hero 区域编辑器

可编辑内容：

- 顶部小标签 (eyebrow)
- 主标题 (title)
- 描述文字 (description)
- 统计数据 (stats) - 支持增删改
- 信号卡片 (signalCard)

#### AboutEditor - 社团简介编辑器

可编辑内容：

- 区块标题
- 区块描述
- 简介卡片列表（增删改）

#### MembersEditor - 成员介绍编辑器

可编辑内容：

- 区块标题
- 区块描述
- 成员小组列表（增删改）

#### ProductsEditor - 产品展示编辑器

可编辑内容：

- 区块标题
- 区块描述
- 分类标签
- 产品章节 (slides) - 支持增删改
- 每个章节内的项目列表

#### OpenSourceEditor - 开源精神编辑器

可编辑内容：

- 区块标题
- 区块描述
- 开源理念卡片
- 加入横幅内容

#### PagesEditor - 子页面管理

- 页面列表、按 slug 编辑、新建（模板）、删除
- 单页「恢复默认」、与 `defaults.py` 对齐
- 预览前将当前编辑态写入 `sessionStorage`，新窗口带 `previewPage` 查询参数

#### SystemEditor - 系统设置

- 飞书通知方式：`webhook` / `app`
- Webhook 地址、应用群 Chat ID
- 展示卡片回调 URL（供复制到飞书开放平台）

#### ApplicationsManager - 报名记录

- 按状态筛选、编辑备注与考核群信息、保存
- 与飞书流程一致的快捷按钮（处理中 / 通过 / 拒绝 / 归档）
- 无未保存修改时定时静默刷新列表

### 功能特性（与实现一致部分）

1. **JWT**：登录后 token 存 `localStorage`，请求自动带 `Authorization`
2. **导入/导出**：调用后端 `/api/admin/export`、`import`，下载/上传 JSON
3. **整站恢复默认**：`POST /api/admin/reset-all`
4. **预览**：`setSitePreview` / `setPagePreview` 写入 `sessionStorage`；前台带查询参数时优先读预览数据
5. **子页面**：`PagesEditor` 支持新建、删除、单页重置、未保存预览与保存
6. **系统设置**：`SystemEditor` 维护 `system`（飞书模式、Webhook、Chat ID、回调说明）
7. **报名记录**：`ApplicationsManager` 筛选、编辑、快捷动作、定时静默刷新
8. **图片**：`ImageUploadField` + `uploadImage` 对接 `/api/admin/upload-image`

侧边栏除首页各区块编辑器外，还包括：**子页面管理**、**报名记录**、**系统设置**，以及导出/导入/恢复默认。

---

## 前端 API 服务（api.js）

源码：`src/services/api.js`。`API_BASE` 来自 `import.meta.env.VITE_API_BASE`（默认 `http://localhost:5000/api`）。

### 职责摘要

- **公开读**：`getSiteConfig()` → `GET /config`；`getPage(slug)` → `GET /pages/:slug`（失败时用 `defaultConfig.js` 兜底）
- **预览**：URL 含 `previewSite=1` 或 `previewPage=<slug>` 时从 `sessionStorage` 读预览 JSON
- **鉴权**：`login` / `logout` / `getCurrentUser`；`request()` 在 401/422 时清 token 并 `location.reload()`
- **管理端**：`getAdminConfig`、`updateSiteConfig`、子页面 CRUD、`resetPage`、`resetAllContent`、`uploadImage`、报名 `getApplications` / `updateApplication`
- **Legacy 链接**：`normalizeLegacyData` 将历史 `/pages/xxx.html` 转为 `/xxx` 路由
- **提交报名**：`submitApplication` → `POST /applications`（无需登录）

### 常用方法（参数见源码）


| 分类  | 方法                                                                                                |
| --- | ------------------------------------------------------------------------------------------------- |
| 站点  | `getSiteConfig`, `updateSiteConfig`, `getAdminConfig`                                             |
| 子页  | `getPage`, `getAdminPages`, `getAdminPage`, `updatePage`, `createPage`, `deletePage`, `resetPage` |
| 备份  | `exportAll`, `importAll`, `resetAllContent`                                                       |
| 报名  | `submitApplication`, `getApplications`, `updateApplication`                                       |
| 其他  | `uploadImage`, `setSitePreview`, `setPagePreview`, …                                              |


---

## Vue 子页面

所有子页面已迁移为 Vue 组件，从后端 API 获取动态内容：


| 路由             | 组件                  | 说明    |
| -------------- | ------------------- | ----- |
| `/about`       | AboutView.vue       | 关于我们  |
| `/members`     | MembersView.vue     | 成员介绍  |
| `/projects`    | ProjectsView.vue    | 项目展示  |
| `/blog`        | BlogView.vue        | 博客动态  |
| `/join`        | JoinView.vue        | 加入我们  |
| `/recruitment` | RecruitmentView.vue | 招新信息  |
| `/open-source` | OpenSourceView.vue  | 开源精神  |
| `/timeline`    | TimelineView.vue    | 时间线   |
| `/onboarding`  | OnboardingView.vue  | 新手指南  |
| `/yuji`        | YujiView.vue        | 雨记协作板 |


### 页面数据加载

每个子页面在 `onMounted` 时调用 API 获取内容：

```javascript
onMounted(async () => {
  try {
    const data = await api.getPage('about')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load page:', error)
  }
})
```

如果 API 请求失败，页面会回退到组件内的默认数据。

> **说明**：`public/pages/` 下可为旧书签保留 **跳转到 Vue 路由** 的轻量 HTML（如 `/about`），非必须；新链接应直接使用 `/slug` 路径。

---

## 开发指南

### 新增页面区块

1. 在 `HomeView.vue` 添加 section：

```vue
<section class="section flip-section" id="new-section" data-reveal-section>
  <div class="section-heading flip-heading">
    <p class="eyebrow">NEW SECTION</p>
    <h2>{{ siteConfig.newSection.title }}</h2>
  </div>
  <!-- 内容 -->
</section>
```

1. 在 `defaultConfig.js` 添加数据结构：

```javascript
newSection: {
  title: '新区块标题',
  items: []
}
```

1. 在 `Navbar.vue` 添加导航链接：

```vue
<RouterLink :to="{ name: 'home', hash: '#new-section' }">新区块</RouterLink>
```

1. 在 `AdminView.vue` 添加对应编辑器

### 修改动画效果

编辑对应的 composable 文件：

- 滚动平滑度：`useLenis.js` 的 `duration` 和 `easing`
- 入场动画：`useGsapAnimations.js` 的 `gsap.from()` 参数
- 滚动进度：`useScrollMotion.js` 的计算逻辑

### 添加新组件

1. 在 `src/components/` 创建 `.vue` 文件
2. 在需要的视图中导入使用：

```javascript
import NewComponent from '../components/NewComponent.vue'
```

### 修改站点配置

1. **开发时**：直接修改 `defaultConfig.js`
2. **运行时**：访问 `/admin` 使用可视化编辑器
3. **批量修改**：使用导入/导出功能

---

## 部署说明

生产环境需要同时提供：**Vue 静态资源**、**Flask API**、**公网 HTTPS**（飞书卡片回调、邮件、外链处理页）。

### 1. 构建前端

```bash
npm run build
```

产物在 `dist/`。构建时通过环境变量或 CI 注入 `**VITE_API_BASE**`，应指向用户浏览器可访问的 API 地址，例如 `https://api.yourdomain.com/api` 或同域 `https://yourdomain.com/api`。

若站点部署在子路径，在 `vite.config.js` 设置 `base: '/子路径/'`，并同步调整反向代理。

### 2. 部署后端

```bash
cd backend
pip install -r requirements.txt
# 配置 .env 后
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

（Windows 可继续用 `python app.py` 或 Waitress；生产建议 Linux + Gunicorn + Nginx。）

确保已执行过 `python init_db.py`，且 MySQL 可连。上传目录 `UPLOAD_FOLDER` 需进程可写。

### 3. Nginx 同域反代（推荐）

浏览器只访问 `https://yourdomain.com`：静态走 `dist`，API 反代到 Gunicorn。

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    root /var/www/xingyu/dist;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        proxy_pass http://127.0.0.1:5000/uploads/;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 4. 生产环境变量要点


| 配置                              | 说明                                                               |
| ------------------------------- | ---------------------------------------------------------------- |
| `CORS_ORIGINS`                  | 包含前端页面 origin，如 `https://yourdomain.com`                         |
| `APPLICATION_ACTION_BASE_URL`   | `https://yourdomain.com`（无尾斜杠），供报名处理页与飞书卡片链接                     |
| 飞书回调                            | `https://yourdomain.com/api/feishu/cards/callback` 须在开放平台填写且证书有效 |
| `MAIL_ENABLED` / SMTP           | 报名结果邮件与欢迎邮件                                                      |
| `SECRET_KEY` / `JWT_SECRET_KEY` | 勿使用仓库默认值                                                         |


### 5. Docker Compose 一键部署（推荐）

项目提供了完整的 Docker Compose 配置，包含三个容器：**MySQL**、**Flask 后端**、**Nginx 前端**。

#### 前置条件

- 服务器已安装 Docker 与 Docker Compose
- 已构建前端（`npm run build` 生成 `dist/`）

#### 部署步骤

```bash
# 1. 将项目复制到服务器
scp -r . user@server:/path/to/base_web

# 2. 进入项目目录
cd /path/to/base_web

# 3. 复制环境变量模板并编辑
cp .env.docker .env
vim .env   # 修改下方关键配置
```

#### `.env` 关键配置

```env
# 必须修改
SECRET_KEY=随机字符串
JWT_SECRET_KEY=另一个随机字符串
CORS_ORIGINS=https://your-domain.com
APPLICATION_ACTION_BASE_URL=https://your-domain.com

# 数据库（默认即可，或修改密码）
MYSQL_ROOT_PASSWORD=xingyu_mysql_2026

# 服务端口
APP_PORT=80

# 飞书/邮件按需配置
FEISHU_WEBHOOK_URL=...
MAIL_ENABLED=true
SMTP_SERVER=smtp.qq.com
...
```

#### 启动服务

```bash
# 构建前端
npm install
npm run build

# 启动所有容器（首次会拉取镜像 + 构建后端）
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据卷（慎用，会丢失数据库和上传文件）
docker-compose down -v
```

#### 容器说明

| 服务       | 镜像            | 端口   | 说明                           |
| ---------- | --------------- | ------ | ------------------------------ |
| `db`       | mysql:8.0       | 3306   | MySQL 数据库，数据持久化到 `mysql_data` 卷 |
| `backend`  | 自定义 (Flask)  | 5000   | Flask API，上传文件持久化到 `uploads_data` 卷 |
| `frontend` | nginx:alpine    | 80     | Nginx 托管 `dist/`，反代 `/api` 和 `/uploads` 到后端 |

#### 数据持久化

- **数据库**：`mysql_data` 卷 → 容器内 `/var/lib/mysql`
- **上传文件**：`uploads_data` 卷 → 容器内 `/app/uploads`

`docker-compose down` 不加 `-v` 参数时数据不会丢失。

#### 首次部署后

访问 `http://服务器IP/admin`，使用默认账号登录：

- 用户名：`admin`
- 密码：`admin123`

**请立即修改默认密码。**

#### 常见问题

| 现象 | 排查 |
|------|------|
| 后端启动失败 | `docker-compose logs backend` 查看日志，检查 `.env` 配置 |
| 数据库连接失败 | 确认 `db` 容器健康检查通过：`docker-compose ps` |
| 图片上传后无法显示 | 检查 `uploads_data` 卷是否正常挂载 |
| 飞书回调失败 | 确认 `APPLICATION_ACTION_BASE_URL` 为公网可达地址，且飞书开放平台已配置回调 URL |

### 6. 仅静态托管（不推荐）

若前端托管在纯静态平台且 API 在另一域名，需配置 **CORS** 与 **VITE_API_BASE** 指向 API 域名；飞书回调与 `APPLICATION_ACTION_BASE_URL` 仍须指向 **API 可达的公网地址**。

---

## 版本记录

### v3.2.0 (2026-05-06)

- 新增 Docker Compose 一键部署方案（MySQL + Flask + Nginx）
- 新增项目详情页 `/project/:slug`，支持截图、技术栈、贡献成员展示
- 首页产品展示改为精选项目卡片，数据统一来自 projects 页面
- 管理后台截图编辑器支持文件上传（ImageUploadField）
- 贡献者添加时自动匹配社团成员头像
- 上传接口改为返回相对路径，修复跨环境图片加载问题
- 导航栏补全成员、作品、博客入口
- 成员页增加参与项目关联展示

### v3.1.0 (2026-04-07)

- 文档：补充「快速启动」、环境变量表、完整 API 列表、报名/飞书/邮件说明、前端 `api.js` 说明、部署与 Nginx 示例。
- 功能对齐：系统设置（飞书模式、Webhook、Chat ID、回调 URL 提示）、报名记录与飞书卡片流程、卡片回调 `raw` 响应格式等（以仓库当前代码为准）。

### v3.0.0 (2026-04-06)

**重大更新：全栈 CMS 系统**

- 新增 Flask 后端 API 服务
- MySQL 数据库持久化存储
- JWT 认证的管理后台
- 10 个静态页面迁移为 Vue 组件
- 子页面内容可通过后台编辑
- 数据导入/导出功能

**后端架构：**

- Flask + SQLAlchemy + PyMySQL
- RESTful API 设计
- 公开接口 + 管理接口分离
- 数据库初始化脚本

**前端改进：**

- 新增登录界面
- PagesEditor 子页面管理器
- API 服务重构支持 HTTP 请求
- 路由配置扩展至 12 个页面

### v2.0.0 (2026-04-06)

**新增功能：**

- 全新可视化管理后台系统
- 分区块编辑器（Hero、简介、成员、产品、开源）
- 配置导入/导出功能
- 实时预览面板
- 完善的数据验证机制

**架构改进：**

- 优化 API 服务层结构
- 完善数据配置结构
- 新增管理后台组件目录

### v1.0.0 (2026-04-05)

**初始版本：**

- Vue 3 + Vite 项目框架
- GSAP + Lenis 动画系统
- 首页所有区块实现
- 基础 JSON 编辑器后台
- 静态子页面

---

## 文档信息

- 文档版本：3.2.0
- 最后更新：2026-05-06
- 项目名称：星雨作坊官网 CMS (base_web)
- 分支：vue版本

