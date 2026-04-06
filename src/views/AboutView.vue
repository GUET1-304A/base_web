<template>
  <div class="about-page">
    <Navbar />
    
    <main class="about-main">
      <!-- Hero Section -->
      <section class="about-hero">
        <div class="hero-glow"></div>
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '星辰传承' }}</span>
        <h1 class="hero-title">
          {{ pageData.hero?.title || '星雨' }}
          <span class="title-gradient">{{ pageData.hero?.subtitle ? '' : '作坊' }}</span>
        </h1>
        <p class="hero-subtitle">{{ pageData.hero?.subtitle || '一个重塑代码与设计边界的精英数字共同体' }}</p>
        <div class="hero-badges">
          <div 
            v-for="(badge, index) in (pageData.hero?.badges || defaultBadges)" 
            :key="index"
            class="badge"
          >
            <span class="material-icon">{{ badge.icon }}</span>
            <span>{{ badge.text }}</span>
          </div>
        </div>
      </section>

      <!-- Values Section -->
      <section class="values-section">
        <div class="values-grid">
          <div class="values-header">
            <h2 v-html="formatTitle(pageData.values?.title || '我们的星辰法则')"></h2>
            <p>{{ pageData.values?.subtitle || '源于对极致的渴望，以及对科技生态共同成长的坚定承诺。' }}</p>
          </div>
          <div class="values-cards">
            <div 
              v-for="(item, index) in (pageData.values?.items || defaultValues)" 
              :key="index"
              :class="['value-card', { 'wide': index === 2 }]"
            >
              <div :class="['value-icon', `color-${index}`]">
                <img
                  v-if="item.image"
                  :src="item.image"
                  :alt="item.title"
                  class="value-icon-image"
                />
                <span v-else class="material-icon filled">{{ item.icon }}</span>
              </div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Groups Section -->
      <section class="groups-section">
        <div class="groups-container">
          <div class="groups-header">
            <h2>{{ pageData.groups?.title || '四大星系' }}</h2>
            <p>{{ pageData.groups?.subtitle || '环绕同一颗创意太阳运转的专业智慧节点。' }}</p>
          </div>
          <div class="groups-grid">
            <div 
              v-for="(group, index) in (pageData.groups?.items || defaultGroups)" 
              :key="index"
              :class="['group-card', `group-${index}`]"
            >
              <span class="group-number">{{ String(index + 1).padStart(2, '0') }}</span>
              <div class="group-visual">
                <div :class="['group-orb', `orb-${index}`]"></div>
              </div>
              <h4>{{ group.name }}</h4>
              <span class="group-tag">{{ group.tag }}</span>
              <p>{{ group.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Timeline Section -->
      <section class="timeline-section">
        <div class="timeline-container">
          <div class="timeline-header">
            <span class="timeline-eyebrow">{{ pageData.timeline?.eyebrow || '演进' }}</span>
            <h2 v-html="formatTitle(pageData.timeline?.title || '我们的星际航行')"></h2>
          </div>
          <div class="timeline-content">
            <div 
              v-for="(item, index) in (pageData.timeline?.items || defaultTimeline)" 
              :key="index"
              class="timeline-item"
            >
              <div :class="['timeline-dot', `dot-${index}`]"></div>
              <span :class="['timeline-year', `year-${index}`]">{{ item.year }}</span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta-section">
        <div class="cta-card">
          <div class="cta-glow cta-glow-1"></div>
          <div class="cta-glow cta-glow-2"></div>
          <h2>{{ pageData.cta?.title || '渴望加入这片星群？' }}</h2>
          <p>{{ pageData.cta?.description || '我们始终在寻找具有远见卓识的头脑，以帮助我们绘制数字领域的下一个前沿。' }}</p>
          <div class="cta-buttons">
            <router-link 
              :to="pageData.cta?.primaryButton?.link || '/recruitment'" 
              class="btn-primary"
            >
              {{ pageData.cta?.primaryButton?.text || '查看开放职位' }}
            </router-link>
            <router-link 
              :to="pageData.cta?.secondaryButton?.link || '/join'" 
              class="btn-secondary"
            >
              {{ pageData.cta?.secondaryButton?.text || '咨询作坊' }}
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

const pageData = ref({})

const defaultBadges = [
  { icon: 'stars', text: '始于 2018' },
  { icon: 'hub', text: '四大核心矩阵' }
]

const defaultValues = [
  { icon: 'diamond', title: '匠心独运', description: '像素级的精准。代码级的稳健。我们将每一款产品视为数字宇宙中永恒的艺术品。' },
  { icon: 'public', title: '开源精神', description: '知识属于共同体。我们回馈那些支撑我们创新的代码库，孕育透明开放的文化。' },
  { icon: 'group_work', title: '极致协作', description: '打破工程与艺术的壁垒。我们如同一个统一的神经系统般运转，让个体的光芒放大集体的力量。' }
]

const defaultGroups = [
  { name: '流光', tag: '视觉与动效', description: '掌控光影与运动的物理法则，打造触动感官的沉浸式数字品牌体验。' },
  { name: '星辉', tag: '核心工程', description: '架构的脊梁。构建可扩展、低延迟的系统，驱动高性能的 Web 与移动应用。' },
  { name: '筑云', tag: '云端与运维', description: '优化数字平流层。托管基础设施，自动化部署，以及坚不可摧的安全协议。' },
  { name: '回声', tag: '体验与研究', description: '用户之声。将深度的心理学研究转化为直观的流程与共鸣驱动的交互模型。' }
]

const defaultTimeline = [
  { year: '2018', title: '奇点降临', description: '起初，这只是由三名开发者和一名设计师在地下室作坊组成的公会。使命很简单：创造兼具美感与坚不可摧的事物。' },
  { year: '2021', title: '全球扩张', description: '采用远程优先的组织架构，吸引了横跨三大洲的顶尖人才。这个时代见证了我们四大核心智慧星系的诞生。' },
  { year: '2024', title: '深入云海', description: '转向融合 AI 的生态系统与高度个性化的数字环境。当我们探索可能性的边缘时，这段旅程仍在继续。' }
]

function formatTitle(title) {
  return title.replace(/\s+/, '<br/><span class="text-primary">')  + '</span>'
}

onMounted(async () => {
  try {
    const data = await api.getPage('about')
    if (data) {
      pageData.value = data
    }
  } catch (error) {
    console.warn('Failed to load about page data:', error)
  }
})
</script>

<style scoped>
.about-page {
  background: var(--bg);
  min-height: 100vh;
}

.about-main {
  padding-top: 120px;
}

/* Hero Section */
.about-hero {
  max-width: 1400px;
  margin: 0 auto 160px;
  padding: 0 32px;
  text-align: center;
  position: relative;
}

.hero-glow {
  position: absolute;
  top: -80px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 600px;
  background: radial-gradient(circle, rgba(121, 168, 255, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.hero-eyebrow {
  display: block;
  color: var(--primary);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.hero-title {
  font-size: clamp(48px, 10vw, 120px);
  font-weight: 900;
  letter-spacing: -0.03em;
  line-height: 1;
  margin-bottom: 24px;
  text-shadow: 0 0 60px rgba(121, 168, 255, 0.3);
}

.title-gradient {
  background: linear-gradient(135deg, var(--primary), var(--accent), #d0bcff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  max-width: 640px;
  margin: 0 auto 40px;
  color: var(--muted);
  font-size: 18px;
  line-height: 1.7;
}

.hero-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: rgba(11, 26, 46, 0.7);
  border: 1px solid rgba(121, 168, 255, 0.2);
  border-radius: 999px;
  backdrop-filter: blur(20px);
  font-size: 14px;
  font-weight: 600;
}

.material-icon {
  font-family: 'Material Symbols Outlined';
  font-size: 20px;
  color: var(--primary);
}

.material-icon.filled {
  font-variation-settings: 'FILL' 1;
}

/* Values Section */
.values-section {
  max-width: 1400px;
  margin: 0 auto 200px;
  padding: 0 32px;
}

.values-grid {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 48px;
}

.values-header h2 {
  font-size: 48px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
  line-height: 1.2;
}

.values-header p {
  color: var(--muted);
  font-size: 18px;
  max-width: 400px;
}

.values-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.value-card {
  padding: 40px;
  background: rgba(11, 26, 46, 0.7);
  border: 1px solid rgba(158, 191, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  transition: transform 0.5s ease;
}

.value-card:hover {
  transform: translateY(-8px);
}

.value-card.wide {
  grid-column: span 2;
}

.value-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  margin-bottom: 32px;
  overflow: hidden;
}

.value-icon-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.value-icon.color-0 {
  background: rgba(121, 168, 255, 0.1);
}
.value-icon.color-0 .material-icon {
  color: var(--primary);
}

.value-icon.color-1 {
  background: rgba(130, 209, 236, 0.1);
}
.value-icon.color-1 .material-icon {
  color: #82d1ec;
}

.value-icon.color-2 {
  background: rgba(208, 188, 255, 0.1);
}
.value-icon.color-2 .material-icon {
  color: #d0bcff;
}

.value-card h3 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
}

.value-card p {
  color: var(--muted);
  line-height: 1.7;
}

/* Groups Section */
.groups-section {
  background: rgba(7, 20, 37, 0.8);
  padding: 120px 0;
}

.groups-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

.groups-header {
  text-align: center;
  margin-bottom: 80px;
}

.groups-header h2 {
  font-size: 56px;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin-bottom: 16px;
}

.groups-header p {
  color: var(--muted);
  font-size: 18px;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.group-card {
  position: relative;
  padding: 32px;
  background: var(--panel);
  border-radius: 16px;
  overflow: hidden;
}

.group-card.group-1,
.group-card.group-3 {
  margin-top: 32px;
}

.group-number {
  position: absolute;
  top: 32px;
  right: 32px;
  font-size: 48px;
  font-weight: 900;
  opacity: 0.1;
}

.group-visual {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.group-orb {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  filter: blur(1px);
}

.group-orb.orb-0 {
  background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
}
.group-orb.orb-1 {
  background: radial-gradient(circle, #82d1ec 0%, transparent 70%);
}
.group-orb.orb-2 {
  background: radial-gradient(circle, #d0bcff 0%, transparent 70%);
}
.group-orb.orb-3 {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.6) 0%, transparent 70%);
}

.group-card h4 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.group-tag {
  display: block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.group-card.group-0 .group-tag { color: var(--primary); }
.group-card.group-1 .group-tag { color: #82d1ec; }
.group-card.group-2 .group-tag { color: #d0bcff; }
.group-card.group-3 .group-tag { color: var(--text); }

.group-card p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.7;
}

/* Timeline Section */
.timeline-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 200px 32px;
}

.timeline-container {
  display: flex;
  gap: 80px;
}

.timeline-header {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: 120px;
  height: fit-content;
}

.timeline-eyebrow {
  display: block;
  color: #d0bcff;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.timeline-header h2 {
  font-size: 56px;
  font-weight: 900;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.timeline-content {
  flex: 1;
  border-left: 1px solid rgba(99, 118, 149, 0.3);
  padding-left: 48px;
  display: flex;
  flex-direction: column;
  gap: 120px;
}

.timeline-item {
  position: relative;
}

.timeline-dot {
  position: absolute;
  left: -54px;
  top: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.timeline-dot.dot-0 {
  background: var(--primary);
  box-shadow: 0 0 0 8px rgba(121, 168, 255, 0.1);
}
.timeline-dot.dot-1 {
  background: #82d1ec;
  box-shadow: 0 0 0 8px rgba(130, 209, 236, 0.1);
}
.timeline-dot.dot-2 {
  background: #d0bcff;
  box-shadow: 0 0 0 8px rgba(208, 188, 255, 0.1);
}

.timeline-year {
  display: block;
  font-size: 40px;
  font-weight: 900;
  margin-bottom: 16px;
}

.timeline-year.year-0 { color: var(--primary); }
.timeline-year.year-1 { color: #82d1ec; }
.timeline-year.year-2 { color: #d0bcff; }

.timeline-item h3 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
}

.timeline-item p {
  color: var(--muted);
  font-size: 18px;
  line-height: 1.7;
}

/* CTA Section */
.cta-section {
  max-width: 1400px;
  margin: 0 auto 160px;
  padding: 0 32px;
}

.cta-card {
  position: relative;
  padding: 80px;
  background: rgba(11, 26, 46, 0.7);
  border: 1px solid rgba(158, 191, 255, 0.1);
  border-radius: 24px;
  backdrop-filter: blur(20px);
  text-align: center;
  overflow: hidden;
}

.cta-glow {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  filter: blur(100px);
  pointer-events: none;
}

.cta-glow-1 {
  top: -200px;
  right: -200px;
  background: rgba(121, 168, 255, 0.1);
}

.cta-glow-2 {
  bottom: -200px;
  left: -200px;
  background: rgba(208, 188, 255, 0.1);
}

.cta-card h2 {
  font-size: 48px;
  font-weight: 900;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.cta-card p {
  color: var(--muted);
  font-size: 20px;
  max-width: 560px;
  margin: 0 auto 48px;
  position: relative;
  z-index: 1;
}

.cta-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.btn-primary,
.btn-secondary {
  padding: 16px 40px;
  border-radius: 999px;
  font-size: 18px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: #04101f;
  box-shadow: 0 16px 40px rgba(121, 168, 255, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 50px rgba(121, 168, 255, 0.3);
}

.btn-secondary {
  border: 1px solid var(--panel-border);
  color: var(--text);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 1024px) {
  .values-grid {
    grid-template-columns: 1fr;
  }
  
  .groups-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .group-card.group-1,
  .group-card.group-3 {
    margin-top: 0;
  }
  
  .timeline-container {
    flex-direction: column;
    gap: 48px;
  }
  
  .timeline-header {
    width: 100%;
    position: static;
  }
}

@media (max-width: 640px) {
  .values-cards {
    grid-template-columns: 1fr;
  }
  
  .value-card.wide {
    grid-column: span 1;
  }
  
  .groups-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-card {
    padding: 48px 24px;
  }
}
</style>
