<template>
  <aside class="admin-sidebar">
    <div class="sidebar-header">
      <RouterLink to="/" class="sidebar-brand">
        <span class="brand-mark">XY</span>
        <span class="brand-text">管理后台</span>
      </RouterLink>
    </div>
    
    <nav class="sidebar-nav">
      <div class="nav-section">
        <span class="nav-section-title">首页内容</span>
        <button 
          v-for="item in homeNavItems" 
          :key="item.id"
          :class="['nav-item', { active: activeSection === item.id }]"
          @click="$emit('change-section', item.id)"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </button>
      </div>
      
      <div class="nav-section">
        <span class="nav-section-title">子页面管理</span>
        <button 
          :class="['nav-item', { active: activeSection === 'pages' }]"
          @click="$emit('change-section', 'pages')"
        >
          <span class="nav-icon">📄</span>
          <span class="nav-label">页面列表</span>
        </button>
      </div>

      <div class="nav-section">
        <span class="nav-section-title">报名管理</span>
        <button
          :class="['nav-item', { active: activeSection === 'applications' }]"
          @click="$emit('change-section', 'applications')"
        >
          <span class="nav-icon">📝</span>
          <span class="nav-label">报名记录</span>
        </button>
      </div>

      <div class="nav-section">
        <span class="nav-section-title">系统设置</span>
        <button
          :class="['nav-item', { active: activeSection === 'system' }]"
          @click="$emit('change-section', 'system')"
        >
          <span class="nav-icon">⚙</span>
          <span class="nav-label">通知 Webhook</span>
        </button>
      </div>
      
      <div class="nav-section">
        <span class="nav-section-title">操作</span>
        <button class="nav-item" @click="$emit('export')">
          <span class="nav-icon">↓</span>
          <span class="nav-label">导出数据</span>
        </button>
        <label class="nav-item import-label">
          <span class="nav-icon">↑</span>
          <span class="nav-label">导入数据</span>
          <input type="file" accept=".json" class="hidden-input" @change="handleImport">
        </label>
        <button class="nav-item danger" @click="$emit('reset')">
          <span class="nav-icon">↻</span>
          <span class="nav-label">恢复默认</span>
        </button>
      </div>
    </nav>
    
    <div class="sidebar-footer">
      <RouterLink to="/" class="back-link">
        <span>←</span>
        <span>返回官网</span>
      </RouterLink>
      <button class="logout-btn" @click="$emit('logout')">
        <span>退出登录</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  activeSection: {
    type: String,
    default: 'hero'
  }
})

const emit = defineEmits(['change-section', 'export', 'import', 'reset', 'logout'])

const homeNavItems = [
  { id: 'hero', label: 'Hero 区域', icon: '★' },
  { id: 'about', label: '社团简介', icon: '📋' },
  { id: 'members', label: '成员介绍', icon: '👥' },
  { id: 'products', label: '产品展示', icon: '📦' },
  { id: 'openSource', label: '开源精神', icon: '🌐' },
  { id: 'footer', label: '页脚信息', icon: '📝' }
]

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
  min-height: 100vh;
  background: rgba(8, 16, 30, 0.95);
  border-right: 1px solid var(--panel-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--panel-border);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text);
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
</style>
