<template>
  <header class="admin-header">
    <div class="header-left">
      <h1 class="header-title">{{ sectionTitle }}</h1>
      <span v-if="isDirty" class="unsaved-badge">未保存</span>
    </div>
    
    <div class="header-actions">
      <span v-if="username" class="user-info">
        <span class="user-icon">👤</span>
        <span>{{ username }}</span>
      </span>
      
      <button 
        class="action-btn preview-btn" 
        @click="$emit('preview')"
        title="预览官网效果"
      >
        <span>👁</span>
        <span>预览</span>
      </button>
      
      <button 
        class="action-btn save-btn" 
        :disabled="!isDirty || isSaving"
        @click="$emit('save')"
      >
        <span v-if="isSaving">⏳</span>
        <span v-else>💾</span>
        <span>{{ isSaving ? '保存中...' : '保存' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  activeSection: {
    type: String,
    default: 'hero'
  },
  isDirty: {
    type: Boolean,
    default: false
  },
  isSaving: {
    type: Boolean,
    default: false
  },
  username: {
    type: String,
    default: ''
  }
})

defineEmits(['save', 'preview'])

const sectionTitles = {
  hero: 'Hero 区域编辑',
  about: '社团简介编辑',
  members: '成员介绍编辑',
  products: '产品展示编辑',
  openSource: '开源精神编辑',
  footer: '页脚信息编辑',
  pages: '子页面管理',
  applications: '报名记录管理',
  system: '系统设置'
}

const sectionTitle = computed(() => sectionTitles[props.activeSection] || '内容编辑')
</script>

<style scoped>
.admin-header {
  height: 64px;
  background: rgba(8, 16, 30, 0.9);
  border-bottom: 1px solid var(--panel-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--text);
}

.unsaved-badge {
  padding: 4px 10px;
  background: rgba(255, 180, 50, 0.2);
  color: #ffb432;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: var(--muted);
  font-size: 13px;
}

.user-icon {
  font-size: 14px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(121, 168, 255, 0.3);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.save-btn {
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  color: #03111f;
  border: none;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(121, 168, 255, 0.3);
}
</style>
