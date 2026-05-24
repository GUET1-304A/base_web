<template>
  <div class="project-detail-page">
    <Navbar />

    <main class="project-detail-main">
      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <p>加载中...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="!project" class="not-found">
        <h1>项目未找到</h1>
        <p>该项目可能已被移除或链接无效。</p>
        <router-link to="/projects" class="btn-primary">返回项目列表</router-link>
      </div>

      <template v-else>
        <!-- Hero -->
        <section class="detail-hero">
          <div class="hero-glow"></div>
          <div class="hero-badges">
            <span class="badge-category">{{ project.category }}</span>
            <span v-if="project.status === 'wip'" class="badge-status wip">开发中</span>
            <span v-else-if="project.status === 'archived'" class="badge-status archived">已归档</span>
            <span v-if="project.featured" class="badge-status featured">精选</span>
          </div>
          <h1 class="hero-title">{{ project.name }}</h1>
          <p class="hero-subtitle">{{ project.description }}</p>
          <div v-if="project.startDate" class="hero-meta">
            <span>开始于 {{ project.startDate }}</span>
          </div>
          <div class="hero-actions">
            <a
              v-if="project.githubUrl"
              :href="project.githubUrl"
              target="_blank"
              rel="noreferrer"
              class="btn-primary"
            >
              GitHub 仓库
            </a>
            <a
              v-if="project.demoUrl"
              :href="project.demoUrl"
              target="_blank"
              rel="noreferrer"
              class="btn-secondary"
            >
              在线演示
            </a>
            <router-link
              v-if="project.link && project.link.startsWith('/')"
              :to="project.link"
              class="btn-secondary"
            >
              访问项目
            </router-link>
            <router-link
              v-if="!project.githubUrl && !project.demoUrl && !(project.link && project.link.startsWith('/'))"
              to="/projects"
              class="btn-secondary"
            >
              返回项目列表
            </router-link>
          </div>
        </section>

        <!-- Cover / Screenshots -->
        <section v-if="project.coverImage || project.screenshots?.length" class="detail-screenshots">
          <div class="screenshots-container">
            <div v-if="project.coverImage" class="screenshot-main">
              <img :src="project.coverImage" :alt="project.name" />
            </div>
            <div v-else :class="['screenshot-gradient', project.coverClass || 'aurora']">
              <div class="gradient-overlay"></div>
              <span class="gradient-label">{{ project.name }}</span>
            </div>
            <div v-if="project.screenshots?.length" class="screenshot-list">
              <div
                v-for="(shot, index) in project.screenshots"
                :key="index"
                class="screenshot-item"
              >
                <img :src="shot" :alt="`${project.name} 截图 ${index + 1}`" />
              </div>
            </div>
          </div>
        </section>

        <!-- Tech Stack -->
        <section v-if="project.techStack?.length" class="detail-section">
          <div class="section-container">
            <h2 class="section-title">技术栈</h2>
            <div class="tech-tags">
              <span v-for="(tech, index) in project.techStack" :key="index" class="tech-tag">
                {{ tech }}
              </span>
            </div>
          </div>
        </section>

        <!-- Long Description -->
        <section v-if="project.longDescription" class="detail-section">
          <div class="section-container">
            <h2 class="section-title">项目介绍</h2>
            <div class="long-description">
              <MarkdownRenderer :text="project.longDescription" />
            </div>
          </div>
        </section>

        <!-- Contributors -->
        <section v-if="project.contributors?.length" class="detail-section">
          <div class="section-container">
            <h2 class="section-title">贡献成员</h2>
            <div class="contributors-grid">
              <div
                v-for="(contributor, index) in project.contributors"
                :key="index"
                class="contributor-card"
              >
                <div class="contributor-avatar">
                  <img
                    v-if="contributor.avatar"
                    :src="contributor.avatar"
                    :alt="contributor.name"
                  />
                  <div v-else class="avatar-placeholder">
                    {{ contributor.name?.charAt(0) || '?' }}
                  </div>
                </div>
                <div class="contributor-info">
                  <h3>{{ contributor.name }}</h3>
                  <span class="contributor-role">{{ contributor.role }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Tags -->
        <section v-if="project.tags?.length" class="detail-section">
          <div class="section-container">
            <h2 class="section-title">标签</h2>
            <div class="project-tags">
              <span v-for="(tag, index) in project.tags" :key="index" class="tag">{{ tag }}</span>
            </div>
          </div>
        </section>

        <!-- Related Projects -->
        <section v-if="relatedProjects.length" class="detail-section">
          <div class="section-container">
            <h2 class="section-title">相关项目</h2>
            <div class="related-grid">
              <router-link
                v-for="(related, index) in relatedProjects"
                :key="index"
                :to="`/project/${related.slug}`"
                class="related-card"
              >
                <div :class="['related-cover', related.coverClass || 'aurora']">
                  <img
                    v-if="related.coverImage"
                    :src="related.coverImage"
                    :alt="related.name"
                    class="related-cover-image"
                  />
                </div>
                <div class="related-content">
                  <span class="related-category">{{ related.category }}</span>
                  <h3>{{ related.name }}</h3>
                  <p>{{ related.description }}</p>
                </div>
              </router-link>
            </div>
          </div>
        </section>

        <!-- CTA -->
        <section class="detail-cta">
          <div class="cta-card">
            <h2>对这个项目感兴趣？</h2>
            <p>欢迎加入星雨作坊，参与更多项目的创作。</p>
            <div class="cta-buttons">
              <router-link to="/join" class="btn-primary">加入我们</router-link>
              <router-link to="/projects" class="btn-secondary">查看更多项目</router-link>
            </div>
          </div>
        </section>
      </template>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import MarkdownRenderer from '../components/MarkdownRenderer.vue'

const route = useRoute()
const router = useRouter()

const allProjects = ref([])
const loading = ref(true)

const project = computed(() => {
  return allProjects.value.find(p => p.slug === route.params.slug) || null
})

const relatedProjects = computed(() => {
  if (!project.value) return []
  return allProjects.value
    .filter(p => p.slug !== project.value.slug && p.category === project.value.category)
    .slice(0, 3)
})

async function loadProjects() {
  loading.value = true
  try {
    const data = await api.getPage('projects')
    if (data?.projects) {
      allProjects.value = data.projects
    }
  } catch (error) {
    console.warn('Failed to load project data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadProjects)

watch(() => route.params.slug, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<style scoped>
.project-detail-page {
  background: var(--bg);
  min-height: 100vh;
}

.project-detail-main {
  padding-top: 120px;
}

/* Loading & Not Found */
.loading-state,
.not-found {
  text-align: center;
  padding: 120px 32px;
}

.not-found h1 {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 12px;
}

.not-found p {
  color: var(--muted);
  font-size: 16px;
  margin-bottom: 32px;
}

/* Hero */
.detail-hero {
  max-width: 900px;
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

.hero-badges {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.badge-category {
  padding: 6px 16px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
}

.badge-status {
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge-status.wip {
  background: rgba(255, 183, 77, 0.15);
  color: #ffb74d;
}

.badge-status.archived {
  background: rgba(158, 158, 158, 0.15);
  color: #9e9e9e;
}

.badge-status.featured {
  background: rgba(255, 215, 0, 0.15);
  color: #ffd700;
}

.hero-title {
  font-size: clamp(36px, 7vw, 64px);
  font-weight: 900;
  letter-spacing: -0.03em;
  margin-bottom: 16px;
}

.hero-subtitle {
  color: var(--muted);
  font-size: 18px;
  max-width: 600px;
  margin: 0 auto 16px;
  line-height: 1.6;
}

.hero-meta {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

/* Screenshots */
.detail-screenshots {
  max-width: 1000px;
  margin: 0 auto 80px;
  padding: 0 32px;
}

.screenshots-container {
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--panel-border);
}

.screenshot-main img {
  width: 100%;
  display: block;
}

.screenshot-gradient {
  height: 400px;
  position: relative;
  display: grid;
  place-items: center;
}

.screenshot-gradient.aurora {
  background: linear-gradient(135deg, #4a90e2 0%, #67b26f 100%);
}

.screenshot-gradient.meteor {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.screenshot-gradient.nebula {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.screenshot-gradient.cosmos {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}

.screenshot-gradient.pulse {
  background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
}

.screenshot-gradient.horizon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.gradient-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
}

.gradient-label {
  position: relative;
  z-index: 1;
  font-size: 32px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.screenshot-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 4px;
  padding: 4px;
  background: var(--bg);
}

.screenshot-item img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
  border-radius: 4px;
}

/* Sections */
.detail-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 32px 60px;
}

.section-container {
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 24px;
  background: var(--primary);
  border-radius: 2px;
}

/* Tech Stack */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-tag {
  padding: 8px 18px;
  background: rgba(121, 168, 255, 0.1);
  border: 1px solid rgba(121, 168, 255, 0.2);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: var(--primary);
}

/* Long Description */
.long-description {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.8;
}

/* Contributors */
.contributors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.contributor-card {
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  transition: border-color 0.2s;
}

.contributor-card:hover {
  border-color: var(--primary);
}

.contributor-avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-size: 18px;
  font-weight: 700;
  color: #04101f;
  flex-shrink: 0;
}

.contributor-info h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 2px;
}

.contributor-role {
  font-size: 13px;
  color: var(--muted);
}

/* Tags */
.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  font-size: 13px;
  color: var(--muted);
}

/* Related Projects */
.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.related-card {
  display: block;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s;
}

.related-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
}

.related-cover {
  height: 120px;
  position: relative;
}

.related-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-cover.aurora {
  background: linear-gradient(135deg, #4a90e2 0%, #67b26f 100%);
}

.related-cover.meteor {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.related-cover.nebula {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.related-cover.cosmos {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}

.related-cover.pulse {
  background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
}

.related-cover.horizon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.related-content {
  padding: 16px;
}

.related-category {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(121, 168, 255, 0.12);
  border-radius: 999px;
  font-size: 11px;
  color: var(--primary);
  margin-bottom: 8px;
}

.related-content h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
}

.related-content p {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.5;
}

/* CTA */
.detail-cta {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 32px 120px;
}

.cta-card {
  text-align: center;
  padding: 60px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.cta-card h2 {
  font-size: 30px;
  font-weight: 800;
  margin-bottom: 12px;
}

.cta-card p {
  color: var(--muted);
  font-size: 16px;
  margin-bottom: 32px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  display: inline-block;
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
  .screenshot-gradient {
    height: 240px;
  }

  .gradient-label {
    font-size: 24px;
  }

  .section-container {
    padding: 28px 20px;
  }

  .contributors-grid {
    grid-template-columns: 1fr;
  }

  .related-grid {
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
