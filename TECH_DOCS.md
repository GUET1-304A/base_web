# 星雨作坊官网技术开发文档 v3.0

## 目录

1. [项目概述](#项目概述)
2. [系统架构](#系统架构)
3. [技术栈](#技术栈)
4. [项目结构](#项目结构)
5. [环境配置与运行](#环境配置与运行)
6. [后端 API 服务](#后端-api-服务)
7. [核心模块详解](#核心模块详解)
8. [路由系统](#路由系统)
9. [组件架构](#组件架构)
10. [状态管理](#状态管理)
11. [动画系统](#动画系统)
12. [样式方案](#样式方案)
13. [数据配置](#数据配置)
14. [后台管理系统](#后台管理系统)
15. [API 接口规范](#api-接口规范)
16. [Vue 子页面](#vue-子页面)
17. [开发指南](#开发指南)
18. [部署说明](#部署说明)
19. [版本记录](#版本记录)

---

## 项目概述

星雨作坊官网是一个基于 Vue 3 + Flask 的全栈内容管理系统，作为校园创意社团的官方展示平台。系统采用前后端分离架构，具备流畅的滚动动画、响应式设计、**JWT 认证的后台管理系统**，以及 **MySQL 数据库持久化存储**，支持多终端实时同步更新内容。

### 主要功能

- **品牌首页**：展示社团理念、成员组织、产品作品和开源精神
- **平滑滚动动画**：基于 GSAP 和 Lenis 的沉浸式滚动体验
- **产品轮播**：Tab 切换 + 幻灯片模式展示项目
- **CMS 后台管理**：JWT 认证、可视化编辑官网所有内容、子页面管理
- **动态子页面**：10 个 Vue 组件页面（关于、成员、项目等），内容从后端 API 获取
- **实时预览**：管理后台修改后可实时预览效果
- **数据持久化**：MySQL 数据库存储，支持数据导入/导出

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
│                       数据层                                     │
│  ┌─────────────────┐              ┌─────────────────────────┐   │
│  │   API Service   │              │    数据存储             │   │
│  │   (api.js)      │  ←─────────→ │                         │   │
│  │                 │              │  - localStorage (开发)  │   │
│  │  - getSiteConfig│              │  - 后端API (生产可选)   │   │
│  │  - updateConfig │              │  - JSON文件 (静态)      │   │
│  │  - resetConfig  │              │                         │   │
│  └─────────────────┘              └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 数据流向

```
用户修改 (AdminView)
        │
        ▼
┌───────────────────┐
│  表单验证/处理    │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  API Service      │
│  updateSiteConfig │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  数据存储         │
│  (localStorage)   │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  官网前台刷新     │
│  getSiteConfig    │
└───────────────────┘
```

---

## 技术栈

### 前端


| 类别         | 技术选型                   | 版本      | 用途       |
| ---------- | ---------------------- | ------- | -------- |
| **框架**     | Vue 3                  | ^3.5.30 | 前端核心框架   |
| **路由**     | Vue Router             | ^5.0.4  | SPA 路由管理 |
| **构建工具**   | Vite                   | ^8.0.1  | 开发构建工具   |
| **CSS 框架** | Tailwind CSS           | ^4.2.2  | 原子化 CSS  |
| **动画库**    | GSAP (含 ScrollTrigger) | ^3.14.2 | 高性能动画    |
| **平滑滚动**   | Lenis                  | ^1.3.21 | 平滑滚动体验   |
| **语言**     | JavaScript (ES Module) | -       | 主开发语言    |


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
├── index.html                 # Vite 入口 HTML
├── package.json               # 前端依赖与脚本配置
├── vite.config.js             # Vite 构建配置
├── .env.example               # 前端环境变量模板
├── TECH_DOCS.md               # 技术开发文档
│
├── backend/                   # Flask 后端
│   ├── app.py                 # Flask 应用入口
│   ├── config.py              # 后端配置文件
│   ├── models.py              # 数据库模型（SQLAlchemy）
│   ├── init_db.py             # 数据库初始化脚本
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example           # 后端环境变量模板
│   ├── README.md              # 后端部署文档
│   └── routes/
│       ├── __init__.py
│       ├── api.py             # 公开 API（读取配置/页面）
│       └── admin.py           # 管理 API（CRUD + JWT 认证）
│
├── public/                    # 静态资源目录
│   └── pages/                 # 遗留静态页面（可删除）
│
├── src/
│   ├── main.js                # 应用入口
│   ├── App.vue                # 根组件
│   ├── style.css              # 全局样式主文件
│   ├── router/
│   │   └── index.js           # 路由配置（含 10 个子页面）
│   ├── views/
│   │   ├── HomeView.vue       # 首页视图
│   │   ├── AdminView.vue      # 管理后台（含登录）
│   │   ├── AboutView.vue      # 关于我们
│   │   ├── MembersView.vue    # 成员介绍
│   │   ├── ProjectsView.vue   # 项目展示
│   │   ├── BlogView.vue       # 博客动态
│   │   ├── JoinView.vue       # 加入我们
│   │   ├── RecruitmentView.vue # 招新信息
│   │   ├── OpenSourceView.vue # 开源精神
│   │   ├── TimelineView.vue   # 时间线
│   │   ├── OnboardingView.vue # 新手指南
│   │   └── YujiView.vue       # 雨记协作板
│   ├── components/
│   │   ├── Navbar.vue         # 导航栏组件
│   │   ├── Footer.vue         # 页脚组件
│   │   ├── SkyEffects.vue     # 星空背景效果组件
│   │   └── admin/             # 管理后台组件
│   │       ├── AdminSidebar.vue       # 侧边栏导航
│   │       ├── AdminHeader.vue        # 顶部栏
│   │       ├── HeroEditor.vue         # Hero区编辑器
│   │       ├── AboutEditor.vue        # 简介区编辑器
│   │       ├── MembersEditor.vue      # 成员区编辑器
│   │       ├── ProductsEditor.vue     # 产品区编辑器
│   │       ├── OpenSourceEditor.vue   # 开源区编辑器
│   │       ├── FooterEditor.vue       # 页脚编辑器
│   │       └── PagesEditor.vue        # 子页面管理器
│   ├── composables/
│   │   ├── useLenis.js        # Lenis 平滑滚动
│   │   ├── useGsapAnimations.js  # GSAP 动画
│   │   └── useScrollMotion.js # 滚动状态管理
│   ├── services/
│   │   └── api.js             # API 服务（HTTP 请求 + JWT）
│   └── data/
│       └── defaultConfig.js   # 默认站点配置数据
└── dist/                      # 构建产物（自动生成）
```

---

## 环境配置与运行

### 环境要求

- Node.js >= 18.0.0
- npm >= 9.0.0
- Python >= 3.9
- MySQL >= 5.7

### 前端安装

```bash
npm install
```

### 后端安装

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 数据库配置

1. 创建 MySQL 数据库：

```sql
CREATE DATABASE xingyu_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

1. 配置后端环境变量：

```bash
cd backend
cp .env.example .env
# 编辑 .env 填入 MySQL 连接信息
```

1. 初始化数据库：

```bash
python init_db.py
```

### 启动服务

**1. 启动后端 (端口 5000)**

```bash
cd backend
python app.py
```

**2. 启动前端 (端口 5173)**

```bash
npm run dev
```

### 访问地址

- 官网前台：`http://localhost:5173/`
- 管理后台：`http://localhost:5173/admin`
- 后端 API：`http://localhost:5000/api/`
- 健康检查：`http://localhost:5000/health`

### 默认管理员账号

- 用户名: `admin`
- 密码: `admin123`

> ⚠️ 请在生产环境中修改默认密码！

### 生产构建

```bash
npm run build
```

构建产物输出到 `dist/` 目录

---

## 后端 API 服务

### 数据库模型

```python
# SiteConfig - 站点配置
class SiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(50), unique=True)  # hero, about, members, etc.
    config_value = db.Column(db.JSON)                    # 配置内容
    updated_at = db.Column(db.DateTime)

# Page - 子页面
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)  # about, members, projects
    title = db.Column(db.String(200))
    content = db.Column(db.JSON)                  # 页面内容
    updated_at = db.Column(db.DateTime)

# AdminUser - 管理员
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255))     # Werkzeug 加密
    created_at = db.Column(db.DateTime)
```

### API 端点

**公开接口（无需认证）**


| 方法  | 路径               | 说明       |
| --- | ---------------- | -------- |
| GET | /api/config      | 获取首页站点配置 |
| GET | /api/pages       | 获取所有页面列表 |
| GET | /api/pages/:slug | 获取单个页面内容 |
| GET | /health          | 健康检查     |


**管理接口（需要 JWT）**


| 方法     | 路径                     | 说明      |
| ------ | ---------------------- | ------- |
| POST   | /api/admin/login       | 管理员登录   |
| GET    | /api/admin/me          | 获取当前用户  |
| GET    | /api/admin/config      | 获取站点配置  |
| PUT    | /api/admin/config      | 更新站点配置  |
| PUT    | /api/admin/config/:key | 更新单个配置项 |
| GET    | /api/admin/pages       | 获取所有页面  |
| GET    | /api/admin/pages/:slug | 获取单个页面  |
| PUT    | /api/admin/pages/:slug | 更新页面    |
| DELETE | /api/admin/pages/:slug | 删除页面    |
| GET    | /api/admin/export      | 导出所有数据  |
| POST   | /api/admin/import      | 导入数据    |


### JWT 认证

登录成功后返回 token：

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1...",
  "user": { "id": 1, "username": "admin" }
}
```

后续请求添加 Header：

```
Authorization: Bearer <token>
```

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
    <a class="nav-cta" href="/pages/join.html">加入我们</a>
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
            link: '/pages/onboarding.html',
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
│  AdminHeader (顶部栏)                                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Logo    保存状态    预览按钮    保存按钮    返回官网    │  │
│  └────────────────────────────────────────────────────────┘  │
├─────────┬────────────────────────────────────────────────────┤
│ Sidebar │  主内容区域                                        │
│         │                                                    │
│ ○ Hero  │  ┌─────────────────────────────────────────────┐  │
│ ○ 简介  │  │                                             │  │
│ ○ 成员  │  │           当前选中区块的编辑器               │  │
│ ○ 产品  │  │                                             │  │
│ ○ 开源  │  │           (HeroEditor / AboutEditor / ...)  │  │
│ ○ 页脚  │  │                                             │  │
│         │  └─────────────────────────────────────────────┘  │
│ ─────── │                                                    │
│ ○ 导出  │  ┌─────────────────────────────────────────────┐  │
│ ○ 导入  │  │              实时预览面板                    │  │
│ ○ 重置  │  │           (PreviewPanel 可折叠)             │  │
│         │  └─────────────────────────────────────────────┘  │
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
- 简介卡片列表 - 支持增删改、拖拽排序

#### MembersEditor - 成员介绍编辑器

可编辑内容：

- 区块标题
- 区块描述
- 成员小组列表 - 支持增删改、拖拽排序

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

### 功能特性

1. **实时验证**：表单输入实时校验
2. **自动保存**：可选自动保存草稿到本地
3. **撤销/重做**：支持操作历史
4. **导入/导出**：JSON 配置文件导入导出
5. **预览模式**：编辑时可切换预览
6. **响应式设计**：支持不同设备访问

---

## API 接口规范

### API 服务 (api.js)

```javascript
const CONFIG_KEY = 'xingyu_site_config';

export const api = {
  // 获取全站配置
  async getSiteConfig() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const localData = localStorage.getItem(CONFIG_KEY);
        if (localData) {
          try {
            resolve(JSON.parse(localData));
          } catch (e) {
            resolve(defaultSiteConfig);
          }
        } else {
          resolve(defaultSiteConfig);
        }
      }, 300);
    });
  },

  // 更新全站配置
  async updateSiteConfig(newConfig) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          // 验证配置结构
          if (!validateConfig(newConfig)) {
            reject({ success: false, message: '配置格式不正确' });
            return;
          }
          localStorage.setItem(CONFIG_KEY, JSON.stringify(newConfig));
          resolve({ success: true, message: '配置保存成功' });
        } catch (e) {
          reject({ success: false, message: '保存失败: ' + e.message });
        }
      }, 500);
    });
  },

  // 恢复默认配置
  async resetSiteConfig() {
    return new Promise((resolve) => {
      setTimeout(() => {
        localStorage.removeItem(CONFIG_KEY);
        resolve({ success: true, message: '已恢复默认配置' });
      }, 300);
    });
  },

  // 导出配置为 JSON 文件
  exportConfig() {
    const config = localStorage.getItem(CONFIG_KEY);
    const data = config || JSON.stringify(defaultSiteConfig, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `xingyu-config-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  },

  // 从 JSON 文件导入配置
  async importConfig(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const config = JSON.parse(e.target.result);
          if (!validateConfig(config)) {
            reject({ success: false, message: '配置格式不正确' });
            return;
          }
          localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
          resolve({ success: true, message: '配置导入成功', config });
        } catch (err) {
          reject({ success: false, message: 'JSON 解析失败' });
        }
      };
      reader.onerror = () => reject({ success: false, message: '文件读取失败' });
      reader.readAsText(file);
    });
  }
};

// 配置验证函数
function validateConfig(config) {
  if (!config || typeof config !== 'object') return false;
  const requiredKeys = ['hero', 'about', 'members'];
  return requiredKeys.every(key => key in config);
}
```

### 接口说明


| 方法                         | 说明      | 参数           | 返回值                   |
| -------------------------- | ------- | ------------ | --------------------- |
| `getSiteConfig()`          | 获取站点配置  | -            | `Promise<SiteConfig>` |
| `updateSiteConfig(config)` | 更新站点配置  | `SiteConfig` | `Promise<Result>`     |
| `resetSiteConfig()`        | 重置为默认配置 | -            | `Promise<Result>`     |
| `exportConfig()`           | 导出配置到文件 | -            | `void`                |
| `importConfig(file)`       | 从文件导入配置 | `File`       | `Promise<Result>`     |


### 扩展为真实后端 API

如需连接真实后端，替换为 HTTP 请求：

```javascript
const API_BASE = '/api';

export const api = {
  async getSiteConfig() {
    const response = await fetch(`${API_BASE}/config`);
    if (!response.ok) throw new Error('获取配置失败');
    return response.json();
  },

  async updateSiteConfig(config) {
    const response = await fetch(`${API_BASE}/config`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    if (!response.ok) throw new Error('保存配置失败');
    return response.json();
  },

  async resetSiteConfig() {
    const response = await fetch(`${API_BASE}/config/reset`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error('重置配置失败');
    return response.json();
  }
};
```

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

> **注意**：`public/pages/` 目录的静态 HTML 文件已弃用，可在部署时删除。

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

### 静态部署

```bash
npm run build
```

将 `dist/` 目录部署到任意静态托管服务：

- Vercel
- Netlify
- GitHub Pages
- Nginx / Apache

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /pages/ {
        try_files $uri =404;
    }

    # 管理后台路由
    location /admin {
        try_files $uri /index.html;
    }
}
```

### 环境变量

如需配置 API 基础路径，可在 `vite.config.js` 中设置：

```javascript
export default defineConfig({
  base: '/your-base-path/',
  // ...
})
```

---

## 版本记录

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

- 文档版本：3.0.0
- 最后更新：2026-04-06
- 项目名称：星雨作坊官网 CMS (base_web)
- 分支：vue版本

