<template>
  <div class="yuji-page">
    <Navbar />
    
    <main class="yuji-main">
      <section class="yuji-hero">
        <span class="hero-version">{{ pageData.hero?.version || 'v2.1.0' }}</span>
        <h1>{{ pageData.hero?.title || '雨记协作板' }}</h1>
        <p>{{ pageData.hero?.subtitle || '为小型团队设计的轻量级协作工具' }}</p>
        <div class="hero-metrics">
          <div 
            v-for="(metric, index) in (pageData.hero?.metrics || defaultMetrics)" 
            :key="index"
            class="metric-item"
          >
            <span class="metric-value">{{ metric.value }}</span>
            <span class="metric-label">{{ metric.label }}</span>
          </div>
        </div>
      </section>

      <section class="features-section">
        <h2>{{ pageData.sectionTitles?.features || '功能特性' }}</h2>
        <div class="features-grid">
          <div 
            v-for="(feature, index) in (pageData.features || defaultFeatures)" 
            :key="index"
            class="feature-card"
          >
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <div v-if="feature.tags" class="feature-tags">
              <span v-for="tag in feature.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </section>

      <section class="highlights-section">
        <h2>{{ pageData.sectionTitles?.highlights || '核心亮点' }}</h2>
        <ul class="highlights-list">
          <li v-for="(highlight, index) in (pageData.highlights || defaultHighlights)" :key="index">
            {{ highlight }}
          </li>
        </ul>
      </section>

      <section class="cta-section">
        <div class="cta-card">
          <h2>{{ pageData.cta?.title || '在 GitHub 上查看' }}</h2>
          <a :href="pageData.cta?.link || DEFAULT_GITHUB_URL" class="cta-btn" target="_blank" rel="noreferrer">
            {{ pageData.cta?.buttonText || '查看源码' }}
          </a>
        </div>
      </section>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { DEFAULT_GITHUB_URL } from '../constants/externalLinks.js'

const pageData = ref({})

const defaultMetrics = [
  { value: '1.2k', label: 'Star' },
  { value: '48', label: '贡献者' },
  { value: '12', label: '分支' }
]

const defaultFeatures = [
  { title: '设计初衷', description: '从社团内部需求出发，解决小团队任务管理和进度同步的痛点。', tags: [] },
  { title: '技术架构', description: '前端 Vue 3 + 后端 Rust，追求性能与开发体验的平衡。', tags: ['Vue 3', 'Rust', 'WebSocket'] },
  { title: '开源协议', description: '采用 MIT 协议开源，欢迎社区贡献和二次开发。', tags: [] }
]

const defaultHighlights = [
  '实时协作，多人同时编辑',
  '任务拆分与进度追踪',
  '复盘记录与知识沉淀',
  '轻量部署，开箱即用'
]

onMounted(async () => {
  try {
    const data = await api.getPage('yuji')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load yuji page:', error)
  }
})
</script>

<style scoped>
.yuji-page { background: var(--bg); min-height: 100vh; }
.yuji-main { padding-top: 120px; max-width: 900px; margin: 0 auto; }

.yuji-hero {
  text-align: center;
  padding: 0 32px 80px;
}

.hero-version {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 20px;
}

.yuji-hero h1 {
  font-size: clamp(40px, 8vw, 64px);
  font-weight: 900;
  margin-bottom: 16px;
}

.yuji-hero p {
  color: var(--muted);
  font-size: 18px;
  margin-bottom: 40px;
}

.hero-metrics {
  display: flex;
  justify-content: center;
  gap: 48px;
}

.metric-item {
  text-align: center;
}

.metric-value {
  display: block;
  font-size: 32px;
  font-weight: 800;
  color: var(--primary);
}

.metric-label {
  font-size: 13px;
  color: var(--muted);
}

.features-section {
  padding: 0 32px 60px;
}

.features-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-card {
  padding: 28px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.feature-card p {
  color: var(--muted);
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.feature-tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
}

.highlights-section {
  padding: 0 32px 60px;
}

.highlights-section h2 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 24px;
}

.highlights-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.highlights-list li {
  padding: 20px 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  font-size: 15px;
  position: relative;
  padding-left: 48px;
}

.highlights-list li::before {
  content: '✓';
  position: absolute;
  left: 20px;
  color: var(--primary);
  font-weight: 700;
}

.cta-section { padding: 0 32px 120px; }

.cta-card {
  text-align: center;
  padding: 60px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.cta-card h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
}

.cta-btn {
  display: inline-block;
  padding: 14px 40px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 999px;
  color: #04101f;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(121, 168, 255, 0.25);
}

@media (max-width: 640px) {
  .hero-metrics { flex-direction: column; gap: 24px; }
  .highlights-list { grid-template-columns: 1fr; }
}
</style>
