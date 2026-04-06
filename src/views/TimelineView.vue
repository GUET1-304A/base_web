<template>
  <div class="timeline-page">
    <Navbar />
    
    <main class="timeline-main">
      <section class="timeline-hero">
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '星雨纪事' }}</span>
        <h1>{{ pageData.hero?.title || '星际时间线' }}</h1>
        <p>{{ pageData.hero?.subtitle || '记录我们的每一次探索与成长。' }}</p>
      </section>

      <section v-if="(pageData.upcoming || defaultUpcoming).length" class="upcoming-section">
        <h2>{{ pageData.sections?.upcomingTitle || '即将到来' }}</h2>
        <div class="upcoming-grid">
          <div 
            v-for="(event, index) in (pageData.upcoming || defaultUpcoming)" 
            :key="index"
            class="upcoming-card"
          >
            <span class="event-type">{{ event.type }}</span>
            <h3>{{ event.title }}</h3>
            <p>{{ event.description }}</p>
            <span class="event-date">{{ event.date }}</span>
          </div>
        </div>
      </section>

      <section class="milestones-section">
        <h2>{{ pageData.sections?.milestonesTitle || '里程碑' }}</h2>
        <div class="milestones-list">
          <div 
            v-for="(milestone, index) in (pageData.milestones || defaultMilestones)" 
            :key="index"
            class="milestone-item"
          >
            <div class="milestone-year">{{ milestone.year }}</div>
            <div class="milestone-dot"></div>
            <div class="milestone-content">
              <h3>{{ milestone.title }}</h3>
              <p>{{ milestone.description }}</p>
            </div>
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

const defaultUpcoming = [
  { title: '技术分享会', date: '2024-12-20', type: '讲座', description: '分享 2024 年度技术实践经验' },
  { title: '设计工作坊', date: '2024-12-25', type: '工作坊', description: '设计系统构建实战' }
]

const defaultMilestones = [
  { year: '2024', title: '星雨 3.0 发布', description: '全新的官网与管理系统上线' },
  { year: '2023', title: '开源计划启动', description: '首批开源项目发布到 GitHub' },
  { year: '2022', title: '四大星系成立', description: '组织架构正式确立' },
  { year: '2021', title: '首个产品上线', description: '雨记协作板 1.0 发布' },
  { year: '2018', title: '星雨创立', description: '几位志同道合的同学开始了这段旅程' }
]

onMounted(async () => {
  try {
    const data = await api.getPage('timeline')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load timeline page:', error)
  }
})
</script>

<style scoped>
.timeline-page { background: var(--bg); min-height: 100vh; }
.timeline-main { padding-top: 120px; max-width: 900px; margin: 0 auto; }

.timeline-hero {
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

.timeline-hero h1 {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.timeline-hero p {
  color: var(--muted);
  font-size: 18px;
}

.upcoming-section {
  padding: 0 32px 80px;
}

.upcoming-section h2, .milestones-section h2 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 24px;
}

.upcoming-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.upcoming-card {
  padding: 24px;
  background: rgba(121, 168, 255, 0.08);
  border: 1px solid rgba(121, 168, 255, 0.2);
  border-radius: 16px;
}

.event-type {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.2);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
  margin-bottom: 12px;
}

.upcoming-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.upcoming-card p {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 12px;
}

.event-date {
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
}

.milestones-section {
  padding: 0 32px 120px;
}

.milestones-list {
  position: relative;
  padding-left: 120px;
}

.milestones-list::before {
  content: '';
  position: absolute;
  left: 100px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--panel-border);
}

.milestone-item {
  position: relative;
  padding-bottom: 48px;
}

.milestone-item:last-child { padding-bottom: 0; }

.milestone-year {
  position: absolute;
  left: -120px;
  top: 0;
  width: 80px;
  text-align: right;
  font-size: 20px;
  font-weight: 800;
  color: var(--primary);
}

.milestone-dot {
  position: absolute;
  left: -20px;
  top: 4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: 0 0 0 4px rgba(121, 168, 255, 0.2);
}

.milestone-content {
  padding: 20px 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  margin-left: 16px;
}

.milestone-content h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.milestone-content p {
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 640px) {
  .milestones-list {
    padding-left: 40px;
  }
  
  .milestones-list::before {
    left: 20px;
  }
  
  .milestone-year {
    position: static;
    width: auto;
    text-align: left;
    margin-bottom: 8px;
  }
  
  .milestone-dot {
    left: -26px;
  }
  
  .milestone-content {
    margin-left: 0;
  }
}
</style>
