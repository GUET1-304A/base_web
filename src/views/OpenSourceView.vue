<template>
  <div class="opensource-page">
    <Navbar />
    
    <main class="opensource-main">
      <section class="opensource-hero">
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '开源生态系统' }}</span>
        <h1>{{ pageData.hero?.title || '我们的开源世界' }}</h1>
        <p>{{ pageData.hero?.subtitle || '代码是我们的语言，开源是我们的信仰。' }}</p>
      </section>

      <section class="repos-section">
        <h2>{{ pageData.sections?.reposTitle || '开源仓库' }}</h2>
        <div class="repos-grid">
          <a 
            v-for="(repo, index) in (pageData.repos || defaultRepos)" 
            :key="index"
            class="repo-card"
            :href="repo.link || DEFAULT_GITHUB_URL"
            target="_blank"
            rel="noreferrer"
          >
            <div class="repo-header">
              <h3>{{ repo.name }}</h3>
              <span class="repo-stars">⭐ {{ repo.stars }}</span>
            </div>
            <p>{{ repo.description }}</p>
            <span class="repo-lang">{{ repo.language }}</span>
          </a>
        </div>
      </section>

      <section class="tech-section">
        <h2>{{ pageData.sections?.techStackTitle || '技术栈' }}</h2>
        <div class="tech-tags">
          <span 
            v-for="(tech, index) in (pageData.techStack || defaultTechStack)" 
            :key="index"
            class="tech-tag"
          >
            {{ tech }}
          </span>
        </div>
      </section>

      <section class="contributors-section">
        <h2>{{ pageData.sections?.contributorsTitle || '核心贡献者' }}</h2>
        <div class="contributors-list">
          <div 
            v-for="(contributor, index) in (pageData.contributors || defaultContributors)" 
            :key="index"
            class="contributor-item"
          >
            <img
              v-if="contributor.avatar"
              :src="contributor.avatar"
              :alt="contributor.name"
              class="contributor-avatar-image"
            />
            <div v-else class="contributor-avatar">{{ contributor.name.charAt(0) }}</div>
            <div class="contributor-info">
              <span class="contributor-name">{{ contributor.name }}</span>
              <span class="contributor-commits">{{ contributor.commits }} commits</span>
            </div>
          </div>
        </div>
      </section>

      <section class="community-section">
        <div class="community-card">
          <h2>{{ pageData.community?.title || '加入我们的开源社区' }}</h2>
          <p>{{ pageData.community?.description || '欢迎贡献代码、提交 Issue 或参与讨论' }}</p>
          <div class="community-links">
            <a :href="pageData.community?.github || DEFAULT_GITHUB_URL" class="community-btn" target="_blank" rel="noreferrer">
              {{ pageData.community?.githubText || 'GitHub' }}
            </a>
            <a :href="pageData.community?.discord || '#'" class="community-btn secondary">
              {{ pageData.community?.discordText || 'Discord' }}
            </a>
          </div>
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

const defaultRepos = [
  { name: 'Star-Chart UI', description: '星雨作坊的设计系统与 UI 组件库', stars: 128, language: 'TypeScript' },
  { name: 'Rain-Note Core', description: '雨记协作板的核心引擎', stars: 89, language: 'Rust' },
  { name: 'Celestial CLI', description: '项目脚手架与开发工具集', stars: 56, language: 'Go' }
]

const defaultTechStack = ['Vue', 'React', 'TypeScript', 'Python', 'Rust', 'PostgreSQL', 'Docker']

const defaultContributors = [
  { name: '核心贡献者 A', commits: 234 },
  { name: '核心贡献者 B', commits: 189 },
  { name: '核心贡献者 C', commits: 156 }
]

onMounted(async () => {
  try {
    const data = await api.getPage('open-source')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load open-source page:', error)
  }
})
</script>

<style scoped>
.opensource-page { background: var(--bg); min-height: 100vh; }
.opensource-main { padding-top: 120px; max-width: 1000px; margin: 0 auto; }

.opensource-hero {
  text-align: center;
  padding: 0 32px 80px;
}

.hero-eyebrow {
  display: block;
  color: var(--primary);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.opensource-hero h1 {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.opensource-hero p {
  color: var(--muted);
  font-size: 18px;
}

.repos-section, .tech-section, .contributors-section {
  padding: 0 32px 60px;
}

.repos-section h2, .tech-section h2, .contributors-section h2 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 24px;
}

.repos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.repo-card {
  display: block;
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.repo-card:hover { border-color: var(--primary); transform: translateY(-4px); }

.repo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.repo-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}

.repo-stars {
  font-size: 13px;
  color: var(--muted);
}

.repo-card p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
}

.repo-lang {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tech-tag {
  padding: 10px 20px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 999px;
  font-size: 14px;
  color: var(--text);
}

.contributors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.contributor-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
}

.contributor-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-weight: 700;
  color: #04101f;
}

.contributor-avatar-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}

.contributor-name {
  display: block;
  font-weight: 600;
  font-size: 14px;
}

.contributor-commits {
  font-size: 12px;
  color: var(--muted);
}

.community-section { padding: 0 32px 120px; }

.community-card {
  text-align: center;
  padding: 60px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.community-card h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 12px;
}

.community-card p {
  color: var(--muted);
  font-size: 16px;
  margin-bottom: 28px;
}

.community-links {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.community-btn {
  padding: 12px 28px;
  background: var(--primary);
  border-radius: 999px;
  color: #04101f;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.community-btn:hover { transform: translateY(-2px); }

.community-btn.secondary {
  background: transparent;
  border: 1px solid var(--panel-border);
  color: var(--text);
}
</style>
