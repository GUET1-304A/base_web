<template>
  <div class="site-shell">
    <header class="topbar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">XY</span>
        <span class="brand-text">星雨作坊</span>
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">返回首页</RouterLink>
      </nav>
      <button class="nav-cta" type="button" @click="resetConfig">恢复默认</button>
    </header>

    <main class="section">
      <div class="section-heading">
        <p class="eyebrow">ADMIN</p>
        <h2>站点配置</h2>
        <p>当前版本提供基础的配置查看与保存能力。</p>
      </div>

      <div class="panel" style="margin-top: 28px">
        <h3>配置 JSON</h3>
        <textarea v-model="draft" class="admin-textarea" rows="22"></textarea>
        <div class="hero-actions" style="margin-top: 18px">
          <button class="button button-primary" type="button" @click="saveConfig">保存</button>
          <button class="button button-secondary" type="button" @click="reloadConfig">重新加载</button>
        </div>
        <p v-if="message" class="hero-text" style="margin-top: 14px">{{ message }}</p>
      </div>
    </main>

    <footer class="footer">
      <p>星雨作坊 Xingyu Studio</p>
      <p>以协作连接灵感，以开源延续成长。</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'
import { defaultSiteConfig } from '../data/defaultConfig.js'

const draft = ref(JSON.stringify(defaultSiteConfig, null, 2))
const message = ref('')

const reloadConfig = async () => {
  const config = await api.getSiteConfig()
  draft.value = JSON.stringify(config ?? defaultSiteConfig, null, 2)
  message.value = ''
}

const saveConfig = async () => {
  try {
    const parsed = JSON.parse(draft.value)
    const result = await api.updateSiteConfig(parsed)
    message.value = result?.message ?? '保存成功'
  } catch (e) {
    message.value = 'JSON 格式不正确'
  }
}

const resetConfig = async () => {
  const result = await api.resetSiteConfig()
  draft.value = JSON.stringify(defaultSiteConfig, null, 2)
  message.value = result?.message ?? '已恢复默认'
}

reloadConfig()
</script>

<style scoped>
.admin-textarea {
  width: 100%;
  margin-top: 14px;
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  outline: none;
  resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  line-height: 1.6;
}
</style>
