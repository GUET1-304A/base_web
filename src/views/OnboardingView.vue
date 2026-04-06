<template>
  <div class="onboarding-page">
    <Navbar />
    
    <main class="onboarding-main">
      <section class="onboarding-hero">
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '入职指南' }}</span>
        <h1>{{ pageData.hero?.title || '欢迎加入星雨' }}</h1>
        <p>{{ pageData.hero?.subtitle || '这份指南将帮助你快速融入团队，开始你的星际之旅。' }}</p>
      </section>

      <section class="steps-section">
        <h2>{{ pageData.sections?.stepsTitle || '入职流程' }}</h2>
        <div class="steps-grid">
          <div 
            v-for="(step, index) in (pageData.steps || defaultSteps)" 
            :key="index"
            class="step-card"
          >
            <span class="step-number">{{ index + 1 }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.description }}</p>
          </div>
        </div>
      </section>

      <section class="resources-section">
        <h2>{{ pageData.sections?.resourcesTitle || '资源中心' }}</h2>
        <div class="resources-grid">
          <div 
            v-for="(resource, index) in (pageData.resources || defaultResources)" 
            :key="index"
            class="resource-card"
          >
            <span class="resource-icon">{{ getIcon(resource.icon) }}</span>
            <h3>{{ resource.title }}</h3>
            <p>{{ resource.description }}</p>
          </div>
        </div>
      </section>

      <section class="mentors-section">
        <h2>{{ pageData.sections?.mentorsTitle || '你的导师' }}</h2>
        <div class="mentors-grid">
          <div 
            v-for="(mentor, index) in (pageData.mentors || defaultMentors)" 
            :key="index"
            class="mentor-card"
          >
            <img
              v-if="mentor.avatar"
              :src="mentor.avatar"
              :alt="mentor.name"
              class="mentor-avatar-image"
            />
            <div v-else class="mentor-avatar">{{ mentor.name.charAt(0) }}</div>
            <h3>{{ mentor.name }}</h3>
            <span class="mentor-role">{{ mentor.role }}</span>
            <p>{{ mentor.description }}</p>
          </div>
        </div>
      </section>

      <section class="faq-section">
        <h2>{{ pageData.sections?.faqTitle || '常见问题' }}</h2>
        <div class="faq-list">
          <div 
            v-for="(faq, index) in (pageData.faq || defaultFaq)" 
            :key="index"
            class="faq-item"
          >
            <h4>{{ faq.question }}</h4>
            <p>{{ faq.answer }}</p>
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

const defaultSteps = [
  { title: '提交申请', description: '填写申请表，介绍自己' },
  { title: '面试交流', description: '轻松聊天，互相了解' },
  { title: '试用期', description: '参与小项目，感受氛围' },
  { title: '正式成员', description: '欢迎加入星雨大家庭' }
]

const defaultResources = [
  { title: '内部维基', description: '项目文档、规范指南、学习资料', icon: 'book' },
  { title: '设计资产', description: '品牌素材、UI 组件、设计模板', icon: 'palette' },
  { title: '代码教程', description: '技术栈入门、最佳实践、代码规范', icon: 'code' },
  { title: 'Discord 社区', description: '日常交流、问题讨论、活动通知', icon: 'chat' }
]

const defaultMentors = [
  { name: '导师 A', role: '产品方向', description: '帮助你理解产品思维' },
  { name: '导师 B', role: '技术方向', description: '指导技术成长路径' },
  { name: '导师 C', role: '设计方向', description: '提升设计审美与技能' }
]

const defaultFaq = [
  { question: '试用期多长时间？', answer: '一般 2-4 周，根据项目情况灵活调整。' },
  { question: '如何获取开发环境？', answer: '入职后会收到环境配置指南，导师会协助你完成设置。' },
  { question: '遇到问题找谁？', answer: '可以在 Discord 提问，或直接联系你的导师。' }
]

const iconMap = { book: '📚', palette: '🎨', code: '💻', chat: '💬' }

function getIcon(icon) {
  return iconMap[icon] || '📄'
}

onMounted(async () => {
  try {
    const data = await api.getPage('onboarding')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load onboarding page:', error)
  }
})
</script>

<style scoped>
.onboarding-page { background: var(--bg); min-height: 100vh; }
.onboarding-main { padding-top: 120px; max-width: 1000px; margin: 0 auto; }

.onboarding-hero {
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

.onboarding-hero h1 {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.onboarding-hero p {
  color: var(--muted);
  font-size: 18px;
  max-width: 500px;
  margin: 0 auto;
}

.steps-section, .resources-section, .mentors-section, .faq-section {
  padding: 0 32px 60px;
}

.steps-section h2, .resources-section h2, .mentors-section h2, .faq-section h2 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 24px;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.step-card {
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  text-align: center;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  font-weight: 700;
  color: #04101f;
  margin-bottom: 16px;
}

.step-card h3 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
}

.step-card p {
  color: var(--muted);
  font-size: 13px;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.resource-card {
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
}

.resource-icon {
  font-size: 32px;
  margin-bottom: 12px;
  display: block;
}

.resource-card h3 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
}

.resource-card p {
  color: var(--muted);
  font-size: 13px;
}

.mentors-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.mentor-card {
  padding: 28px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  text-align: center;
}

.mentor-avatar {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-size: 24px;
  font-weight: 700;
  color: #04101f;
}

.mentor-avatar-image {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}

.mentor-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
}

.mentor-role {
  display: block;
  color: var(--primary);
  font-size: 13px;
  margin-bottom: 12px;
}

.mentor-card p {
  color: var(--muted);
  font-size: 14px;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
}

.faq-item h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.faq-item p {
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 768px) {
  .steps-grid { grid-template-columns: repeat(2, 1fr); }
  .resources-grid { grid-template-columns: 1fr; }
  .mentors-grid { grid-template-columns: 1fr; }
}
</style>
