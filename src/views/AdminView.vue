<template>
  <div
    :class="[
      'admin-layout',
      {
        'sidebar-collapsed': isSidebarCollapsed,
        'sidebar-compact': isCompactViewport
      }
    ]"
  >
    <!-- 登录界面 -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>星雨作坊</h1>
          <p>内容管理系统</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>用户名</label>
            <input 
              v-model="loginForm.username" 
              type="text" 
              placeholder="请输入用户名"
              :disabled="isLoggingIn"
            />
          </div>
          
          <div class="form-group">
            <label>密码</label>
            <input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码"
              :disabled="isLoggingIn"
            />
          </div>
          
          <div v-if="loginError" class="login-error">
            {{ loginError }}
          </div>
          
          <button type="submit" class="login-btn" :disabled="isLoggingIn">
            <span v-if="isLoggingIn">登录中...</span>
            <span v-else>登录</span>
          </button>
        </form>
      </div>
    </div>
    
    <!-- 管理界面 -->
    <template v-else>
      <AdminSidebar 
        :active-section="activeSection"
        :collapsed="isSidebarCollapsed"
        :is-compact="isCompactViewport"
        :is-open="isSidebarOpen"
        @change-section="changeSection"
        @export="handleExport"
        @import="handleImport"
        @reset="handleReset"
        @logout="handleLogout"
        @toggle="toggleSidebar"
      />

      <div
        v-if="isCompactViewport && isSidebarOpen"
        class="sidebar-backdrop"
        @click="closeSidebar"
      ></div>
      
      <div class="admin-main">
        <AdminHeader 
          :active-section="activeSection"
          :is-dirty="isDirty"
          :is-saving="isSaving"
          :username="currentUser?.username"
          :sidebar-collapsed="isSidebarCollapsed"
          :is-compact="isCompactViewport"
          @save="handleSave"
          @preview="handlePreview"
          @toggle-sidebar="toggleSidebar"
        />
        
        <main class="admin-content">
          <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>加载配置中...</p>
          </div>
          
          <template v-else-if="siteConfig">
            <HeroEditor 
              v-if="activeSection === 'hero'"
              v-model="siteConfig.hero"
              @update:model-value="markDirty"
            />
            
            <AboutEditor 
              v-else-if="activeSection === 'about'"
              v-model="siteConfig.about"
              @update:model-value="markDirty"
            />
            
            <MembersEditor 
              v-else-if="activeSection === 'members'"
              v-model="siteConfig.members"
              @update:model-value="markDirty"
            />
            
            <ProductsEditor 
              v-else-if="activeSection === 'products'"
              v-model="siteConfig.products"
              @update:model-value="markDirty"
            />
            
            <OpenSourceEditor 
              v-else-if="activeSection === 'openSource'"
              v-model="siteConfig.openSource"
              @update:model-value="markDirty"
            />
            
            <FooterEditor 
              v-else-if="activeSection === 'footer'"
              v-model="siteConfig.footer"
              @update:model-value="markDirty"
            />
            
            <PagesEditor
              v-else-if="activeSection === 'pages'"
              ref="pagesEditorRef"
              :refresh-token="pagesRefreshToken"
              @update="markDirty"
            />

            <ApplicationsManager
              v-else-if="activeSection === 'applications'"
            />

            <SystemEditor
              v-else-if="activeSection === 'system'"
              v-model="siteConfig.system"
              @update:model-value="markDirty"
            />
          </template>
          
          <div v-else class="error-state">
            <p>加载配置失败，请刷新页面重试</p>
          </div>
        </main>
        
        <div v-if="message" :class="['toast', messageType]">
          {{ message }}
        </div>
      </div>
      
      <div v-if="showPreview" class="preview-modal" @click.self="showPreview = false">
        <div class="preview-container">
          <div class="preview-header">
            <h3>预览效果</h3>
            <button class="close-btn" @click="showPreview = false">×</button>
          </div>
          <iframe ref="previewFrame" :src="previewUrl" class="preview-iframe"></iframe>
        </div>
      </div>
      
      <div v-if="showResetConfirm" class="confirm-modal" @click.self="showResetConfirm = false">
        <div class="confirm-dialog">
          <h3>确认恢复默认内容？</h3>
          <p>此操作将清除所有首页配置和子页面内容，恢复为系统默认值。此操作不可撤销。</p>
          <div class="confirm-actions">
            <button class="btn-cancel" @click="showResetConfirm = false">取消</button>
            <button class="btn-confirm" @click="confirmReset">确认恢复</button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { api } from '../services/api.js'
import AdminSidebar from '../components/admin/AdminSidebar.vue'
import AdminHeader from '../components/admin/AdminHeader.vue'
import HeroEditor from '../components/admin/HeroEditor.vue'
import AboutEditor from '../components/admin/AboutEditor.vue'
import MembersEditor from '../components/admin/MembersEditor.vue'
import ProductsEditor from '../components/admin/ProductsEditor.vue'
import OpenSourceEditor from '../components/admin/OpenSourceEditor.vue'
import FooterEditor from '../components/admin/FooterEditor.vue'
import PagesEditor from '../components/admin/PagesEditor.vue'
import ApplicationsManager from '../components/admin/ApplicationsManager.vue'
import SystemEditor from '../components/admin/SystemEditor.vue'

const isLoggedIn = ref(false)
const currentUser = ref(null)
const loginForm = ref({ username: '', password: '' })
const loginError = ref('')
const isLoggingIn = ref(false)

const siteConfig = ref(null)
const activeSection = ref('hero')
const isDirty = ref(false)
const isLoading = ref(true)
const isSaving = ref(false)
const message = ref('')
const messageType = ref('success')
const showPreview = ref(false)
const showResetConfirm = ref(false)
const previewUrl = ref('/')
const pagesRefreshToken = ref(0)
const pagesEditorRef = ref(null)
const isSidebarCollapsed = ref(false)
const isCompactViewport = ref(false)
const isSidebarOpen = ref(true)

async function handleLogin() {
  if (isLoggingIn.value) return
  
  loginError.value = ''
  isLoggingIn.value = true
  
  try {
    const result = await api.login(loginForm.value.username, loginForm.value.password)
    currentUser.value = result.user
    isLoggedIn.value = true
    await loadConfig()
  } catch (error) {
    loginError.value = error.message || '登录失败，请检查用户名和密码'
  } finally {
    isLoggingIn.value = false
  }
}

function handleLogout() {
  api.logout()
  isLoggedIn.value = false
  currentUser.value = null
  siteConfig.value = null
  loginForm.value = { username: '', password: '' }
}

async function checkAuth() {
  if (api.isLoggedIn()) {
    try {
      currentUser.value = await api.getCurrentUser()
      isLoggedIn.value = true
      await loadConfig()
    } catch (error) {
      api.logout()
      isLoggedIn.value = false
    }
  }
}

function changeSection(section) {
  activeSection.value = section
  if (isCompactViewport.value) {
    isSidebarOpen.value = false
  }
}

function markDirty() {
  isDirty.value = true
}

function showMessage(text, type = 'success') {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

async function loadConfig() {
  isLoading.value = true
  try {
    siteConfig.value = await api.getSiteConfig()
    if (!siteConfig.value.system) {
      siteConfig.value.system = {
        feishuWebhookUrl: ''
      }
    }
  } catch (e) {
    showMessage('加载配置失败', 'error')
  } finally {
    isLoading.value = false
  }
}

async function handleSave() {
  if (activeSection.value === 'pages' && pagesEditorRef.value?.triggerHeaderSave) {
    await pagesEditorRef.value.triggerHeaderSave()
    return
  }

  if (isSaving.value) return
  isSaving.value = true
  
  try {
    await api.updateSiteConfig(siteConfig.value)
    isDirty.value = false
    showMessage('配置保存成功！')
  } catch (e) {
    showMessage(e.message || '保存失败', 'error')
  } finally {
    isSaving.value = false
  }
}

function handlePreview() {
  if (activeSection.value === 'pages' && pagesEditorRef.value?.triggerHeaderPreview) {
    pagesEditorRef.value.triggerHeaderPreview()
    return
  }

  api.setSitePreview(siteConfig.value)
  showPreview.value = true
  previewUrl.value = '/?previewSite=1&t=' + Date.now()
}

async function handleExport() {
  try {
    await api.exportAll()
    showMessage('数据已导出')
  } catch (e) {
    showMessage('导出失败', 'error')
  }
}

async function handleImport(file) {
  try {
    const result = await api.importAll(file)
    await loadConfig()
    showMessage(result.message || '数据导入成功！')
  } catch (e) {
    showMessage(e.message || '导入失败', 'error')
  }
}

function handleReset() {
  showResetConfirm.value = true
}

async function confirmReset() {
  try {
    await api.resetAllContent()
    await loadConfig()
    pagesRefreshToken.value += 1
    isDirty.value = false
    showResetConfirm.value = false
    showMessage('已恢复首页配置和所有子页面默认内容')
  } catch (e) {
    showMessage('恢复失败', 'error')
  }
}

function syncSidebarState() {
  const compact = window.innerWidth <= 1024
  isCompactViewport.value = compact
  if (compact) {
    isSidebarCollapsed.value = false
    isSidebarOpen.value = false
    return
  }
  isSidebarOpen.value = true
}

function toggleSidebar() {
  if (isCompactViewport.value) {
    isSidebarOpen.value = !isSidebarOpen.value
    return
  }
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

function closeSidebar() {
  if (isCompactViewport.value) {
    isSidebarOpen.value = false
  }
}

function handleBeforeUnload(e) {
  if (isDirty.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}

onMounted(() => {
  checkAuth()
  syncSidebarState()
  window.addEventListener('beforeunload', handleBeforeUnload)
  window.addEventListener('resize', syncSidebarState)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
  window.removeEventListener('resize', syncSidebarState)
})
</script>

<style scoped>
.admin-layout {
  --admin-sidebar-width: 260px;
  display: flex;
  min-height: 100vh;
  background: var(--bg);
}

.admin-layout.sidebar-collapsed {
  --admin-sidebar-width: 88px;
}

.login-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: radial-gradient(ellipse at center, rgba(30, 60, 114, 0.3) 0%, var(--bg) 70%);
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(12, 24, 42, 0.9);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 48px 40px;
  backdrop-filter: blur(20px);
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.login-header h1 {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 600;
  color: var(--text);
  background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.7) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-header p {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

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

.form-group input {
  padding: 14px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(0, 0, 0, 0.5);
}

.form-group input::placeholder {
  color: var(--muted);
}

.login-error {
  padding: 12px 16px;
  background: rgba(255, 100, 100, 0.1);
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 10px;
  color: #ff6b6b;
  font-size: 13px;
}

.login-btn {
  margin-top: 8px;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary) 0%, #5b8def 100%);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(74, 144, 226, 0.3);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.admin-main {
  flex: 1;
  margin-left: var(--admin-sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  transition: margin-left 0.24s ease;
}

.admin-content {
  flex: 1;
  padding: 32px;
  width: 100%;
  max-width: 1400px;
  box-sizing: border-box;
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 90;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: var(--muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--panel-border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  z-index: 200;
  animation: slideIn 0.3s ease;
}

.toast.success {
  background: rgba(50, 200, 120, 0.9);
  color: #fff;
}

.toast.error {
  background: rgba(255, 100, 100, 0.9);
  color: #fff;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.preview-modal,
.confirm-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
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

.confirm-dialog {
  background: rgba(12, 24, 42, 0.95);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  padding: 28px;
  max-width: 420px;
  text-align: center;
}

.confirm-dialog h3 {
  margin: 0 0 12px;
  color: var(--text);
}

.confirm-dialog p {
  margin: 0 0 24px;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel,
.btn-confirm {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  border: 1px solid var(--panel-border);
  background: transparent;
  color: var(--text);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
}

.btn-confirm {
  border: none;
  background: #ff6b6b;
  color: #fff;
}

.btn-confirm:hover {
  background: #ff5252;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
  }
  
  .admin-content {
    padding: 20px;
  }
}
</style>
