<template>
  <div class="pages-editor">
    <!-- 页面列表视图 -->
    <div v-if="!editingPage && !showCreateForm" class="pages-list">
      <div class="pages-header">
        <div class="header-left">
          <h2>子页面管理</h2>
          <p class="pages-desc">管理官网的所有子页面内容，点击页面进入可视化编辑</p>
        </div>
        <button class="create-page-btn" @click="showCreateForm = true">
          + 新建页面
        </button>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载页面列表...</p>
      </div>
      
      <div v-else class="pages-grid">
        <div 
          v-for="page in pages" 
          :key="page.slug"
          class="page-card"
          @click="openPage(page.slug)"
        >
          <div class="page-icon">{{ getPageIcon(page.slug) }}</div>
          <div class="page-info">
            <h3>{{ page.title }}</h3>
            <span class="page-slug">/{{ page.slug }}</span>
            <span class="page-updated" v-if="page.updated_at">
              更新于 {{ formatDate(page.updated_at) }}
            </span>
          </div>
          <div class="page-actions">
            <button class="preview-btn" @click.stop="previewPage(page.slug)" title="预览">
              👁
            </button>
            <button class="delete-btn" @click.stop="confirmDeletePage(page.slug, page.title)" title="删除">
              🗑
            </button>
            <span class="page-arrow">→</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创建页面表单 -->
    <div v-else-if="showCreateForm" class="create-form">
      <div class="form-header">
        <button class="back-btn" @click="showCreateForm = false">
          <span>←</span>
          <span>返回列表</span>
        </button>
        <h2>创建新页面</h2>
      </div>
      
      <div class="form-content">
        <div class="form-group">
          <label>页面路径 (slug)</label>
          <div class="slug-input">
            <span class="slug-prefix">/</span>
            <input 
              v-model="newPage.slug" 
              type="text" 
              placeholder="my-page"
              @input="validateSlug"
            />
          </div>
          <span v-if="slugError" class="input-error">{{ slugError }}</span>
          <span class="input-hint">仅支持小写字母、数字和连字符</span>
        </div>
        
        <div class="form-group">
          <label>页面标题</label>
          <input v-model="newPage.title" type="text" placeholder="我的页面" />
        </div>
        
        <div class="form-group">
          <label>初始内容模板</label>
          <select v-model="newPage.template">
            <option value="blank">空白页面</option>
            <option value="basic">基础模板 (Hero + CTA)</option>
            <option value="article">文章模板</option>
          </select>
        </div>
        
        <div class="form-actions">
          <button class="cancel-btn" @click="showCreateForm = false">取消</button>
          <button 
            class="create-btn" 
            :disabled="!canCreatePage || creatingPage"
            @click="createPage"
          >
            {{ creatingPage ? '创建中...' : '创建页面' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 页面编辑视图 -->
    <div v-else class="page-editor">
      <div class="editor-header">
        <button class="back-btn" @click="closePage">
          <span>←</span>
          <span>返回列表</span>
        </button>
        <div class="editor-title">
          <h2>{{ currentPage?.title || '编辑页面' }}</h2>
          <span class="page-route">/{{ editingPage }}</span>
        </div>
        <div class="editor-header-actions">
          <button class="reset-page-btn" @click="resetCurrentPage">
            ↻ 恢复默认
          </button>
          <button class="preview-btn-large" @click="previewPage(editingPage)">
            👁 预览
          </button>
        </div>
      </div>
      
      <div v-if="pageLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载页面内容...</p>
      </div>
      
      <div v-else-if="currentPage" class="editor-content">
        <!-- 编辑模式切换 -->
        <div class="edit-mode-tabs">
          <button 
            :class="['mode-tab', { active: editMode === 'visual' }]"
            @click="editMode = 'visual'"
          >
            📝 可视化编辑
          </button>
          <button 
            :class="['mode-tab', { active: editMode === 'json' }]"
            @click="switchToJsonMode"
          >
            { } JSON 编辑
          </button>
        </div>
        
        <!-- 可视化编辑模式 -->
        <div v-if="editMode === 'visual'" class="visual-editor">
          <div class="form-section">
            <h3>基本信息</h3>
            <div class="form-group">
              <label>页面标题</label>
              <input v-model="currentPage.title" type="text" @input="markPageDirty" />
            </div>
          </div>
          
          <!-- 根据页面类型显示不同的编辑器 -->
          <component 
            :is="getPageEditorComponent(editingPage)"
            v-model="currentPage.content"
            @update:model-value="markPageDirty"
          />
        </div>
        
        <!-- JSON 编辑模式 -->
        <div v-else class="json-mode">
          <div class="form-group">
            <label>页面标题</label>
            <input v-model="currentPage.title" type="text" @input="markPageDirty" />
          </div>
          
          <div class="form-group">
            <label>
              页面内容 (JSON)
              <span class="json-hint">提示：修改后请确保 JSON 格式正确</span>
            </label>
            <div class="json-editor-wrapper">
              <textarea 
                v-model="contentJson" 
                class="json-editor"
                rows="30"
                @input="handleJsonChange"
              ></textarea>
              <div v-if="jsonError" class="json-error">{{ jsonError }}</div>
            </div>
          </div>
        </div>
        
        <!-- 保存操作 -->
        <div class="editor-actions">
          <span v-if="isPageDirty" class="unsaved-hint">有未保存的更改</span>
          <button 
            class="cancel-btn"
            @click="closePage"
          >
            取消
          </button>
          <button 
            class="save-page-btn" 
            :disabled="!isPageDirty || savingPage || !!jsonError"
            @click="savePage"
          >
            {{ savingPage ? '保存中...' : '保存页面' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 预览弹窗 -->
    <div v-if="showPreview" class="preview-modal" @click.self="showPreview = false">
      <div class="preview-container">
        <div class="preview-header">
          <h3>预览: {{ previewTitle }}</h3>
          <button class="close-btn" @click="showPreview = false">×</button>
        </div>
        <iframe :src="previewUrl" class="preview-iframe"></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw, watch } from 'vue'
import { api } from '../../services/api.js'
import AboutPageEditor from './pages/AboutPageEditor.vue'
import MembersPageEditor from './pages/MembersPageEditor.vue'
import ProjectsPageEditor from './pages/ProjectsPageEditor.vue'
import BlogPageEditor from './pages/BlogPageEditor.vue'
import JoinPageEditor from './pages/JoinPageEditor.vue'
import RecruitmentPageEditor from './pages/RecruitmentPageEditor.vue'
import OpenSourcePageEditor from './pages/OpenSourcePageEditor.vue'
import TimelinePageEditor from './pages/TimelinePageEditor.vue'
import OnboardingPageEditor from './pages/OnboardingPageEditor.vue'
import YujiPageEditor from './pages/YujiPageEditor.vue'
import GenericPageEditor from './pages/GenericPageEditor.vue'

const props = defineProps({
  refreshToken: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update'])

const pages = ref([])
const loading = ref(true)
const editingPage = ref(null)
const currentPage = ref(null)
const pageLoading = ref(false)
const savingPage = ref(false)
const isPageDirty = ref(false)
const contentJson = ref('')
const jsonError = ref('')
const editMode = ref('visual')
const showPreview = ref(false)
const previewUrl = ref('')
const previewTitle = ref('')
const showCreateForm = ref(false)
const creatingPage = ref(false)
const slugError = ref('')
const newPage = ref({
  slug: '',
  title: '',
  template: 'blank'
})

const pageEditors = {
  about: markRaw(AboutPageEditor),
  members: markRaw(MembersPageEditor),
  projects: markRaw(ProjectsPageEditor),
  blog: markRaw(BlogPageEditor),
  join: markRaw(JoinPageEditor),
  recruitment: markRaw(RecruitmentPageEditor),
  'open-source': markRaw(OpenSourcePageEditor),
  timeline: markRaw(TimelinePageEditor),
  onboarding: markRaw(OnboardingPageEditor),
  yuji: markRaw(YujiPageEditor)
}

const pageIcons = {
  about: '📋',
  members: '👥',
  projects: '📦',
  blog: '📝',
  join: '🤝',
  recruitment: '📢',
  'open-source': '🌐',
  timeline: '📅',
  onboarding: '🚀',
  yuji: '🛠️'
}

const pageDescriptions = {
  about: '关于我们 - Hero区、价值观、四大星系、时间线',
  members: '成员介绍 - 成员列表、统计数据',
  projects: '项目展示 - 项目卡片、筛选分类',
  blog: '博客动态 - 文章列表、分类标签',
  join: '加入我们 - 表单说明、小组选择、FAQ',
  recruitment: '招新信息 - 招募流程、小组介绍',
  'open-source': '开源精神 - 仓库列表、贡献者、技术栈',
  timeline: '时间线 - 活动日程、里程碑',
  onboarding: '新手指南 - 入职流程、资源、导师',
  yuji: '雨记协作板 - 产品介绍、功能特点'
}

function getPageIcon(slug) {
  return pageIcons[slug] || '📄'
}

function getPageEditorComponent(slug) {
  return pageEditors[slug] || markRaw(GenericPageEditor)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function loadPages() {
  loading.value = true
  try {
    pages.value = await api.getAdminPages()
  } catch (error) {
    console.error('Failed to load pages:', error)
  } finally {
    loading.value = false
  }
}

async function openPage(slug) {
  editingPage.value = slug
  pageLoading.value = true
  jsonError.value = ''
  editMode.value = 'visual'
  
  try {
    const data = await api.getAdminPage(slug)
    currentPage.value = data
    contentJson.value = JSON.stringify(data.content, null, 2)
    isPageDirty.value = false
  } catch (error) {
    console.error('Failed to load page:', error)
  } finally {
    pageLoading.value = false
  }
}

function closePage() {
  if (isPageDirty.value && !confirm('有未保存的更改，确定要离开吗？')) {
    return
  }
  editingPage.value = null
  currentPage.value = null
  isPageDirty.value = false
  jsonError.value = ''
}

function markPageDirty() {
  isPageDirty.value = true
  if (editMode.value === 'visual') {
    contentJson.value = JSON.stringify(currentPage.value.content, null, 2)
  }
}

function switchToJsonMode() {
  contentJson.value = JSON.stringify(currentPage.value.content, null, 2)
  editMode.value = 'json'
}

function handleJsonChange() {
  isPageDirty.value = true
  jsonError.value = ''
  
  try {
    currentPage.value.content = JSON.parse(contentJson.value)
  } catch (e) {
    jsonError.value = 'JSON 格式错误: ' + e.message
  }
}

function previewPage(slug) {
  if (currentPage.value && editingPage.value === slug) {
    api.setPagePreview(slug, {
      title: currentPage.value.title,
      content: currentPage.value.content
    })
    previewTitle.value = currentPage.value.title || slug
  } else {
    const page = pages.value.find(p => p.slug === slug)
    previewTitle.value = page?.title || slug
  }
  previewUrl.value = `/${slug}?previewPage=${slug}&t=${Date.now()}`
  showPreview.value = true
}

async function savePage() {
  if (jsonError.value) {
    alert('请先修复 JSON 格式错误')
    return
  }
  
  savingPage.value = true
  
  try {
    await api.updatePage(editingPage.value, {
      title: currentPage.value.title,
      content: currentPage.value.content
    })
    isPageDirty.value = false
    emit('update')
    
    await loadPages()
  } catch (error) {
    alert('保存失败: ' + (error.message || '未知错误'))
  } finally {
    savingPage.value = false
  }
}

async function resetCurrentPage() {
  if (!editingPage.value) return
  if (!confirm('确定要将当前子页面恢复为默认内容吗？未保存的修改将丢失。')) {
    return
  }

  try {
    await api.resetPage(editingPage.value)
    await openPage(editingPage.value)
    await loadPages()
    emit('update')
  } catch (error) {
    alert('恢复失败: ' + (error.message || '未知错误'))
  }
}

const canCreatePage = computed(() => {
  return newPage.value.slug && 
         newPage.value.title && 
         !slugError.value &&
         !pages.value.find(p => p.slug === newPage.value.slug)
})

function validateSlug() {
  const slug = newPage.value.slug
  if (!slug) {
    slugError.value = ''
    return
  }
  if (!/^[a-z0-9-]+$/.test(slug)) {
    slugError.value = '仅支持小写字母、数字和连字符'
    return
  }
  if (pages.value.find(p => p.slug === slug)) {
    slugError.value = '该路径已存在'
    return
  }
  slugError.value = ''
}

function getTemplateContent(template) {
  const templates = {
    blank: {},
    basic: {
      hero: {
        title: '页面标题',
        subtitle: '页面副标题描述'
      },
      cta: {
        title: '准备好开始了吗？',
        buttonText: '了解更多',
        buttonLink: '/'
      }
    },
    article: {
      hero: {
        title: '文章标题',
        subtitle: '文章简介',
        date: new Date().toISOString().split('T')[0]
      },
      content: {
        sections: [
          {
            type: 'text',
            content: '在这里添加文章内容...'
          }
        ]
      }
    }
  }
  return templates[template] || {}
}

async function createPage() {
  if (!canCreatePage.value) return
  
  creatingPage.value = true
  try {
    await api.createPage(newPage.value.slug, {
      title: newPage.value.title,
      content: getTemplateContent(newPage.value.template)
    })
    
    showCreateForm.value = false
    newPage.value = { slug: '', title: '', template: 'blank' }
    await loadPages()
    
    openPage(newPage.value.slug || pages.value[pages.value.length - 1]?.slug)
  } catch (error) {
    alert('创建失败: ' + (error.message || '未知错误'))
  } finally {
    creatingPage.value = false
  }
}

async function confirmDeletePage(slug, title) {
  if (!confirm(`确定要删除页面 "${title}" (/\${slug}) 吗？此操作不可恢复。`)) {
    return
  }
  
  try {
    await api.deletePage(slug)
    await loadPages()
    emit('update')
  } catch (error) {
    alert('删除失败: ' + (error.message || '未知错误'))
  }
}

function triggerHeaderPreview() {
  if (!editingPage.value) {
    alert('请先打开一个子页面再预览')
    return
  }
  previewPage(editingPage.value)
}

async function triggerHeaderSave() {
  if (!editingPage.value) {
    alert('请先打开一个子页面再保存')
    return
  }
  await savePage()
}

onMounted(() => {
  loadPages()
})

watch(() => props.refreshToken, async () => {
  await loadPages()
  if (editingPage.value) {
    await openPage(editingPage.value)
  }
})

defineExpose({
  triggerHeaderPreview,
  triggerHeaderSave
})
</script>

<style scoped>
.pages-editor {
  max-width: 900px;
}

.pages-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}

.header-left h2 {
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 700;
  color: var(--text);
}

.pages-desc {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}

.create-page-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  color: #03111f;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.create-page-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(121, 168, 255, 0.3);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--muted);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--panel-border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pages-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.page-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--primary);
  transform: translateX(4px);
}

.page-icon {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  background: rgba(121, 168, 255, 0.1);
  border-radius: 14px;
  font-size: 26px;
  flex-shrink: 0;
}

.page-info {
  flex: 1;
  min-width: 0;
}

.page-info h3 {
  margin: 0 0 4px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text);
}

.page-slug {
  display: block;
  font-size: 13px;
  color: var(--primary);
  font-family: monospace;
  margin-bottom: 4px;
}

.page-updated {
  display: block;
  font-size: 12px;
  color: var(--muted);
}

.page-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: transparent;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--primary);
}

.delete-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: rgba(255, 100, 100, 0.1);
  border-color: rgba(255, 100, 100, 0.5);
}

.page-arrow {
  font-size: 20px;
  color: var(--muted);
  transition: transform 0.2s;
}

.page-card:hover .page-arrow {
  transform: translateX(4px);
  color: var(--primary);
}

/* Editor Header */
.editor-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--panel-border);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--primary);
}

.editor-title {
  flex: 1;
}

.editor-title h2 {
  margin: 0 0 4px;
  font-size: 22px;
  color: var(--text);
}

.page-route {
  font-size: 13px;
  color: var(--primary);
  font-family: monospace;
}

.editor-header-actions {
  display: flex;
  gap: 12px;
}

.preview-btn-large {
  padding: 10px 18px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-btn-large:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--primary);
}

.reset-page-btn {
  padding: 10px 18px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-page-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #ffb432;
  color: #ffb432;
}

/* Edit Mode Tabs */
.edit-mode-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 6px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  width: fit-content;
}

.mode-tab {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-tab:hover {
  color: var(--text);
}

.mode-tab.active {
  background: var(--primary);
  color: #04101f;
}

/* Visual Editor */
.visual-editor {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section h3::before {
  content: '';
  width: 4px;
  height: 16px;
  background: var(--primary);
  border-radius: 2px;
}

/* JSON Mode */
.json-mode {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.json-hint {
  font-size: 12px;
  font-weight: 400;
  color: var(--muted);
  margin-left: 8px;
}

/* Form Elements */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.form-group input,
.form-group select {
  padding: 12px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary);
}

.json-editor-wrapper {
  position: relative;
}

.json-editor {
  width: 100%;
  padding: 16px;
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  color: var(--text);
  font-size: 13px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  line-height: 1.6;
  resize: vertical;
  min-height: 400px;
}

.json-editor:focus {
  outline: none;
  border-color: var(--primary);
}

.json-error {
  margin-top: 10px;
  padding: 12px 16px;
  background: rgba(255, 100, 100, 0.1);
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 10px;
  color: #ff6b6b;
  font-size: 13px;
}

/* Editor Actions */
.editor-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  padding-top: 24px;
  margin-top: 24px;
  border-top: 1px solid var(--panel-border);
}

.unsaved-hint {
  flex: 1;
  font-size: 13px;
  color: #ffb432;
}

.cancel-btn {
  padding: 12px 24px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.05);
}

.save-page-btn {
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  color: #03111f;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.save-page-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(121, 168, 255, 0.3);
}

.save-page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Preview Modal */
.preview-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.preview-container {
  width: 90vw;
  height: 85vh;
  background: var(--bg);
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--panel-border);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(12, 24, 42, 0.9);
  border-bottom: 1px solid var(--panel-border);
}

.preview-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text);
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--text);
  font-size: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.preview-iframe {
  flex: 1;
  border: none;
  background: var(--bg);
}

/* Create Form */
.create-form {
  max-width: 500px;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.form-header h2 {
  margin: 0;
  font-size: 22px;
  color: var(--text);
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-content .form-group {
  margin-bottom: 0;
}

.slug-input {
  display: flex;
  align-items: center;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.slug-prefix {
  padding: 12px 0 12px 14px;
  color: var(--muted);
  font-family: monospace;
}

.slug-input input {
  flex: 1;
  padding: 12px 14px 12px 4px;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  font-family: monospace;
}

.slug-input input:focus {
  outline: none;
}

.input-error {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #ff6b6b;
}

.input-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: var(--muted);
}

.form-content select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
}

.form-content select:focus {
  outline: none;
  border-color: var(--primary);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--panel-border);
}

.create-btn {
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  color: #03111f;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.create-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(121, 168, 255, 0.3);
}

.create-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
