<template>
  <div class="members-page">
    <Navbar />
    
    <main class="members-main">
      <!-- Hero Section -->
      <section class="members-hero">
        <div class="hero-glow"></div>
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '核心星群' }}</span>
        <h1 class="hero-title">{{ pageData.hero?.title || '认识我们的团队' }}</h1>
        <p class="hero-subtitle">{{ pageData.hero?.subtitle || '每一颗星都有独特的光芒，共同组成星雨的银河。' }}</p>
      </section>

      <!-- Stats Section -->
      <section class="stats-section">
        <div class="stats-grid">
          <div 
            v-for="(stat, index) in (pageData.stats || defaultStats)" 
            :key="index"
            class="stat-card"
          >
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </section>

      <!-- Members Grid -->
      <section class="members-list-section">
        <div class="members-container">
          <div class="members-grid">
            <div 
              v-for="(member, index) in (pageData.members || defaultMembers)" 
              :key="index"
              class="member-card"
            >
              <div class="member-avatar">
                <img 
                  v-if="member.avatar" 
                  :src="member.avatar" 
                  :alt="member.name"
                />
                <div v-else class="avatar-placeholder">
                  {{ member.name?.charAt(0) || '?' }}
                </div>
              </div>
              <div class="member-info">
                <h3>{{ member.name }}</h3>
                <span class="member-role">{{ member.role }}</span>
                <span class="member-group">{{ member.group }}</span>
                <p class="member-desc">{{ member.description }}</p>
                <div class="member-skills">
                  <span 
                    v-for="(skill, sIndex) in member.skills" 
                    :key="sIndex"
                    class="skill-tag"
                  >
                    {{ skill }}
                  </span>
                </div>
                <div class="member-links">
                  <a 
                    :href="member.links?.github || DEFAULT_GITHUB_URL" 
                    target="_blank"
                    rel="noreferrer"
                    class="link-btn"
                  >
                    GitHub
                  </a>
                  <a 
                    v-if="member.links?.portfolio" 
                    :href="member.links.portfolio" 
                    target="_blank"
                    class="link-btn"
                  >
                    作品集
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Join CTA -->
      <section class="join-section">
        <div class="join-card">
          <h2>{{ pageData.joinCta?.title || '想成为我们的一员？' }}</h2>
          <p>{{ pageData.joinCta?.description || '我们欢迎志同道合的伙伴加入星雨作坊' }}</p>
          <div class="join-buttons">
            <router-link :to="pageData.joinCta?.primaryButton?.link || '/join'" class="btn-primary">
              {{ pageData.joinCta?.primaryButton?.text || '加入我们' }}
            </router-link>
            <router-link :to="pageData.joinCta?.secondaryButton?.link || '/recruitment'" class="btn-secondary">
              {{ pageData.joinCta?.secondaryButton?.text || '查看招新' }}
            </router-link>
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

const defaultStats = [
  { value: '12+', label: '核心成员' },
  { value: '45+', label: '活跃贡献者' },
  { value: '156k', label: '代码行数' }
]

const defaultMembers = [
  {
    name: '张三',
    role: '产品负责人',
    group: '流光组',
    avatar: '',
    description: '专注于产品战略与用户体验设计',
    skills: ['产品设计', '用户研究', '项目管理'],
    links: { github: '', portfolio: '' }
  },
  {
    name: '李四',
    role: '技术负责人',
    group: '逐云组',
    avatar: '',
    description: '全栈工程师，热衷于开源项目',
    skills: ['Vue', 'Python', 'DevOps'],
    links: { github: '', portfolio: '' }
  },
  {
    name: '王五',
    role: '设计负责人',
    group: '星绘组',
    avatar: '',
    description: 'UI/UX 设计师，追求像素完美',
    skills: ['UI设计', '品牌设计', '动效设计'],
    links: { github: '', portfolio: '' }
  }
]

onMounted(async () => {
  try {
    const data = await api.getPage('members')
    if (data) {
      pageData.value = data
    }
  } catch (error) {
    console.warn('Failed to load members page data:', error)
  }
})
</script>

<style scoped>
.members-page {
  background: var(--bg);
  min-height: 100vh;
}

.members-main {
  padding-top: 120px;
}

/* Hero */
.members-hero {
  max-width: 1200px;
  margin: 0 auto 80px;
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

/* Stats */
.stats-section {
  max-width: 900px;
  margin: 0 auto 80px;
  padding: 0 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.stat-card {
  text-align: center;
  padding: 32px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
}

.stat-value {
  display: block;
  font-size: 48px;
  font-weight: 900;
  color: var(--primary);
  margin-bottom: 8px;
}

.stat-label {
  color: var(--muted);
  font-size: 14px;
}

/* Members Grid */
.members-list-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px 120px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.member-card {
  display: flex;
  gap: 20px;
  padding: 28px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.member-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
}

.member-avatar {
  flex-shrink: 0;
}

.member-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-size: 28px;
  font-weight: 700;
  color: #04101f;
}

.member-info {
  flex: 1;
}

.member-info h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
}

.member-role {
  display: block;
  color: var(--primary);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.member-group {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(121, 168, 255, 0.1);
  border-radius: 999px;
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 12px;
}

.member-desc {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.member-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.skill-tag {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 999px;
  font-size: 12px;
  color: var(--text);
}

.member-links {
  display: flex;
  gap: 12px;
}

.link-btn {
  padding: 6px 14px;
  background: transparent;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  color: var(--muted);
  font-size: 13px;
  text-decoration: none;
  transition: all 0.2s;
}

.link-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

/* Join Section */
.join-section {
  max-width: 900px;
  margin: 0 auto 120px;
  padding: 0 32px;
}

.join-card {
  text-align: center;
  padding: 64px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.join-card h2 {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 12px;
}

.join-card p {
  color: var(--muted);
  font-size: 18px;
  margin-bottom: 32px;
}

.join-buttons {
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
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .members-grid {
    grid-template-columns: 1fr;
  }
  
  .member-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .member-skills {
    justify-content: center;
  }
  
  .member-links {
    justify-content: center;
  }
}
</style>
