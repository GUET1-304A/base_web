<template>
  <div class="projects-page">
    <Navbar />
    
    <main class="projects-main">
      <!-- Hero Section -->
      <section class="projects-hero">
        <div class="hero-glow"></div>
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '策展阶段 04' }}</span>
        <h1 class="hero-title">{{ pageData.hero?.title || '产品画廊' }}</h1>
        <p class="hero-subtitle">{{ pageData.hero?.subtitle || '探索我们精心打造的数字作品集，每一件都承载着创新与匠心。' }}</p>
      </section>

      <!-- Filter Section -->
      <section class="filter-section">
        <div class="filter-container">
          <button 
            v-for="filter in (pageData.filters || defaultFilters)" 
            :key="filter"
            :class="['filter-btn', { active: activeFilter === filter }]"
            @click="activeFilter = filter"
          >
            {{ filter }}
          </button>
        </div>
      </section>

      <!-- Projects Grid -->
      <section class="projects-grid-section">
        <div class="projects-container">
          <div class="projects-grid">
            <router-link 
              v-for="(project, index) in filteredProjects" 
              :key="index"
              :to="project.link || '#'"
              class="project-card"
            >
              <div :class="['project-cover', project.coverClass || 'aurora']">
                <img
                  v-if="project.coverImage"
                  :src="project.coverImage"
                  :alt="project.name"
                  class="project-cover-image"
                />
                <div class="cover-gradient"></div>
              </div>
              <div class="project-content">
                <span class="project-category">{{ project.category }}</span>
                <h3>{{ project.name }}</h3>
                <p>{{ project.description }}</p>
                <div class="project-tags">
                  <span 
                    v-for="(tag, tIndex) in project.tags" 
                    :key="tIndex"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta-section">
        <div class="cta-card">
          <h2>{{ pageData.cta?.title || '想要参与我们的项目？' }}</h2>
          <p>{{ pageData.cta?.description || '我们欢迎各种形式的贡献，从代码到设计，从文档到创意。' }}</p>
          <div class="cta-buttons">
            <router-link 
              :to="pageData.cta?.primaryButton?.link || '/open-source'" 
              class="btn-primary"
            >
              {{ pageData.cta?.primaryButton?.text || '查看贡献指南' }}
            </router-link>
            <router-link 
              :to="pageData.cta?.secondaryButton?.link || '/join'" 
              class="btn-secondary"
            >
              {{ pageData.cta?.secondaryButton?.text || '加入社团' }}
            </router-link>
          </div>
        </div>
      </section>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const pageData = ref({})
const activeFilter = ref('全部')

const defaultFilters = ['全部', '网页', '工具', '品牌']

const defaultProjects = [
  {
    name: '星图导航',
    category: '网页',
    description: '为新成员与访客整理社团资讯的门户网站',
    coverClass: 'aurora',
    link: '/onboarding',
    tags: ['Vue', 'Tailwind']
  },
  {
    name: '雨记协作板',
    category: '工具',
    description: '支持任务拆分、进度同步的轻量化协作工具',
    coverClass: 'meteor',
    link: '/yuji',
    tags: ['React', 'Node.js']
  },
  {
    name: '星雨年刊',
    category: '品牌',
    description: '沉淀年度作品与社团故事的数字刊物',
    coverClass: 'nebula',
    link: '/timeline',
    tags: ['设计', '内容']
  }
]

const filteredProjects = computed(() => {
  const projects = pageData.value.projects || defaultProjects
  if (activeFilter.value === '全部') {
    return projects
  }
  return projects.filter(p => p.category === activeFilter.value)
})

onMounted(async () => {
  try {
    const data = await api.getPage('projects')
    if (data) {
      pageData.value = data
    }
  } catch (error) {
    console.warn('Failed to load projects page data:', error)
  }
})
</script>

<style scoped>
.projects-page {
  background: var(--bg);
  min-height: 100vh;
}

.projects-main {
  padding-top: 120px;
}

/* Hero */
.projects-hero {
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 32px;
  text-align: center;
  position: relative;
}

.hero-glow {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 500px;
  background: radial-gradient(circle, rgba(121, 168, 255, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.hero-eyebrow {
  display: block;
  color: var(--primary);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.hero-title {
  font-size: clamp(40px, 8vw, 72px);
  font-weight: 900;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}

.hero-subtitle {
  color: var(--muted);
  font-size: 18px;
  max-width: 560px;
  margin: 0 auto;
}

/* Filter */
.filter-section {
  max-width: 1200px;
  margin: 0 auto 48px;
  padding: 0 32px;
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.filter-btn {
  padding: 10px 24px;
  border: 1px solid var(--panel-border);
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: var(--primary);
  color: var(--text);
}

.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #04101f;
}

/* Projects Grid */
.projects-grid-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px 100px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.project-card {
  display: block;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s ease;
}

.project-card:hover {
  border-color: var(--primary);
  transform: translateY(-8px);
}

.project-cover {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.project-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.project-cover.aurora {
  background: linear-gradient(135deg, #4a90e2 0%, #67b26f 100%);
}

.project-cover.meteor {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.project-cover.nebula {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.project-cover.cosmos {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}

.project-cover.pulse {
  background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
}

.project-cover.horizon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.cover-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(5, 14, 28, 0.8) 0%, transparent 50%);
}

.project-content {
  padding: 24px;
}

.project-category {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
  margin-bottom: 12px;
}

.project-content h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 8px;
}

.project-content p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  font-size: 12px;
  color: var(--muted);
}

/* CTA Section */
.cta-section {
  max-width: 900px;
  margin: 0 auto 120px;
  padding: 0 32px;
}

.cta-card {
  text-align: center;
  padding: 64px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.cta-card h2 {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 12px;
}

.cta-card p {
  color: var(--muted);
  font-size: 18px;
  margin-bottom: 32px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn-primary,
.btn-secondary {
  padding: 14px 32px;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #04101f;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(121, 168, 255, 0.25);
}

.btn-secondary {
  border: 1px solid var(--panel-border);
  color: var(--text);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-card {
    padding: 40px 24px;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
}
</style>
