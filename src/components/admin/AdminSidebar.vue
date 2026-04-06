<template>
  <aside
    :class="[
      'admin-sidebar',
      { collapsed, compact: isCompact, open: isOpen }
    ]"
  >
    <div class="sidebar-header">
      <RouterLink to="/" class="sidebar-brand">
        <span class="brand-mark">XY</span>
        <span v-if="!collapsed" class="brand-text">管理后台</span>
      </RouterLink>
    </div>
    
    <nav class="sidebar-nav">
      <div class="nav-section">
        <span v-if="!collapsed" class="nav-section-title">首页内容</span>
        <button 
          v-for="item in homeNavItems" 
          :key="item.id"
          :class="['nav-item', { active: activeSection === item.id }]"
          :title="collapsed ? item.label : ''"
          @click="selectSection(item.id)"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </button>
      </div>
      
      <div class="nav-section">
        <span v-if="!collapsed" class="nav-section-title">子页面管理</span>
        <button 
          :class="['nav-item', { active: activeSection === 'pages' }]"
          :title="collapsed ? '页面列表' : ''"
          @click="selectSection('pages')"
        >
          <span class="nav-icon">📄</span>
          <span v-if="!collapsed" class="nav-label">页面列表</span>
        </button>
      </div>

      <div class="nav-section">
        <span v-if="!collapsed" class="nav-section-title">报名管理</span>
        <button
          :class="['nav-item', { active: activeSection === 'applications' }]"
          :title="collapsed ? '报名记录' : ''"
          @click="selectSection('applications')"
        >
          <span class="nav-icon">📝</span>
          <span v-if="!collapsed" class="nav-label">报名记录</span>
        </button>
      </div>

      <div class="nav-section">
        <span v-if="!collapsed" class="nav-section-title">系统设置</span>
        <button
          :class="['nav-item', { active: activeSection === 'system' }]"
          :title="collapsed ? '通知 Webhook' : ''"
          @click="selectSection('system')"
        >
          <span class="nav-icon">⚙</span>
          <span v-if="!collapsed" class="nav-label">通知 Webhook</span>
        </button>
      </div>
      
      <div class="nav-section">
        <span v-if="!collapsed" class="nav-section-title">操作</span>
        <button class="nav-item" :title="collapsed ? '导出数据' : ''" @click="$emit('export')">
          <span class="nav-icon">↓</span>
          <span v-if="!collapsed" class="nav-label">导出数据</span>
        </button>
        <label class="nav-item import-label">
          <span class="nav-icon">↑</span>
          <span v-if="!collapsed" class="nav-label">导入数据</span>
          <input type="file" accept=".json" class="hidden-input" @change="handleImport">
        </label>
        <button class="nav-item danger" :title="collapsed ? '恢复默认' : ''" @click="$emit('reset')">
          <span class="nav-icon">↻</span>
          <span v-if="!collapsed" class="nav-label">恢复默认</span>
        </button>
      </div>
    </nav>
    
    <div class="sidebar-footer">
      <RouterLink to="/" class="back-link">
        <span>⌂</span>
        <span v-if="!collapsed">返回官网</span>
      </RouterLink>
      <button class="logout-btn" @click="$emit('logout')">
        <span>{{ collapsed ? '⎋' : '退出登录' }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  activeSection: {
    type: String,
    default: 'hero'
  },
  collapsed: {
    type: Boolean,
    default: false
  },
  isCompact: {
    type: Boolean,
    default: false
  },
  isOpen: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['change-section', 'export', 'import', 'reset', 'logout', 'toggle'])

const homeNavItems = [
  { id: 'hero', label: 'Hero 区域', icon: '★' },
  { id: 'about', label: '社团简介', icon: '📋' },
  { id: 'members', label: '成员介绍', icon: '👥' },
  { id: 'products', label: '产品展示', icon: '📦' },
  { id: 'openSource', label: '开源精神', icon: '🌐' },
  { id: 'footer', label: '页脚信息', icon: '📝' }
]

function selectSection(section) {
  emit('change-section', section)
}

function handleImport(e) {
  const file = e.target.files?.[0]
  if (file) {
    emit('import', file)
    e.target.value = ''
  }
}
</script>

<style scoped>
.admin-sidebar {
  width: 260px;
  height: 100vh;
  background: rgba(8, 16, 30, 0.95);
  border-right: 1px solid var(--panel-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  overflow: hidden;
  transition: width 0.24s ease, transform 0.24s ease;
}

.admin-sidebar.collapsed {
  width: 88px;
}

.admin-sidebar.compact {
  width: min(280px, calc(100vw - 32px));
  transform: translateX(-100%);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
}

.admin-sidebar.compact.open {
  transform: translateX(0);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--panel-border);
  display: flex;
  align-items: center;
  gap: 0;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text);
  min-width: 0;
}

.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #04101f;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 14px;
}

.brand-text {
  font-weight: 700;
  font-size: 16px;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
  min-height: 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(121, 168, 255, 0.55) rgba(255, 255, 255, 0.05);
}

.sidebar-nav::-webkit-scrollbar {
  width: 10px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 999px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(121, 168, 255, 0.75), rgba(91, 141, 239, 0.55));
  border: 2px solid rgba(8, 16, 30, 0.95);
  border-radius: 999px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(121, 168, 255, 0.9), rgba(91, 141, 239, 0.75));
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section-title {
  display: block;
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}

.nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: var(--muted);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.admin-sidebar.collapsed .nav-item,
.admin-sidebar.collapsed .back-link,
.admin-sidebar.collapsed .logout-btn {
  justify-content: center;
}

.admin-sidebar.collapsed .nav-item {
  padding: 12px;
}

.nav-item:hover {
  background: rgba(121, 168, 255, 0.08);
  color: var(--text);
}

.nav-item.active {
  background: rgba(121, 168, 255, 0.15);
  color: var(--primary);
}

.nav-item.danger:hover {
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
}

.nav-icon {
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.import-label {
  cursor: pointer;
}

.hidden-input {
  display: none;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--panel-border);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary);
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 100, 100, 0.1);
  border-color: rgba(255, 100, 100, 0.3);
  color: #ff6b6b;
}

@media (max-width: 1024px) {
  .admin-sidebar {
    width: min(280px, calc(100vw - 32px));
  }
}
</style>
