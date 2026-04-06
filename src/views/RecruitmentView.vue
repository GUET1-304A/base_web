<template>
  <div class="recruitment-page">
    <Navbar />
    
    <main class="recruitment-main">
      <section class="recruitment-hero">
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '2024 年度招募' }}</span>
        <h1>{{ pageData.hero?.title || '新星招募计划' }}</h1>
        <p>{{ pageData.hero?.subtitle || '寻找下一代数字创作者，共同书写星雨的未来篇章。' }}</p>
      </section>

      <section class="groups-section">
        <div class="groups-grid">
          <div 
            v-for="(group, index) in (pageData.groups || defaultGroups)" 
            :key="index"
            class="group-card"
          >
            <span class="group-tag">{{ group.tag }}</span>
            <h3>{{ group.name }}</h3>
            <p>{{ group.description }}</p>
            <div class="requirements">
              <h4>我们期望你：</h4>
              <ul>
                <li v-for="(req, rIndex) in group.requirements" :key="rIndex">{{ req }}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section class="process-section">
        <h2>{{ pageData.sectionTitles?.process || '招募流程' }}</h2>
        <div class="process-steps">
          <div 
            v-for="(step, index) in (pageData.process || defaultProcess)" 
            :key="index"
            class="step-item"
          >
            <span class="step-number">{{ index + 1 }}</span>
            <div class="step-content">
              <h4>{{ step.step }}</h4>
              <p>{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="cta-section">
        <div class="cta-card">
          <h2>{{ pageData.cta?.title || '准备好加入了吗？' }}</h2>
          <router-link 
            :to="pageData.cta?.buttonLink || '/join'" 
            class="cta-btn"
          >
            {{ pageData.cta?.buttonText || '立即投递申请' }}
          </router-link>
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

const defaultGroups = [
  { name: '流光组', tag: '产品策划', description: '如果你善于洞察需求、组织思路、推动项目落地，这里是你的舞台。', requirements: ['对互联网产品有热情', '良好的逻辑思维', '沟通协调能力'] },
  { name: '星绘组', tag: '视觉设计', description: '如果你追求像素完美、热爱视觉表达，来和我们一起创造美。', requirements: ['熟悉设计工具', '有审美追求', '愿意接受反馈'] },
  { name: '逐云组', tag: '技术开发', description: '如果你热爱代码、追求技术精进，这里有真实的项目等你挑战。', requirements: ['编程基础', '学习能力强', '喜欢解决问题'] },
  { name: '回声组', tag: '内容传播', description: '如果你擅长表达、热爱分享，帮助我们让作品被更多人看见。', requirements: ['文字功底', '社媒运营兴趣', '创意思维'] }
]

const defaultProcess = [
  { step: '投递申请', description: '填写申请表，告诉我们你的故事' },
  { step: '初步筛选', description: '我们会认真阅读每份申请' },
  { step: '面试交流', description: '轻松的聊天，互相了解' },
  { step: '试用期', description: '参与一个小项目，感受氛围' }
]

onMounted(async () => {
  try {
    const data = await api.getPage('recruitment')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load recruitment page:', error)
  }
})
</script>

<style scoped>
.recruitment-page { background: var(--bg); min-height: 100vh; }
.recruitment-main { padding-top: 120px; max-width: 1100px; margin: 0 auto; }

.recruitment-hero {
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

.recruitment-hero h1 {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.recruitment-hero p {
  color: var(--muted);
  font-size: 18px;
  max-width: 500px;
  margin: 0 auto;
}

.groups-section { padding: 0 32px 80px; }

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.group-card {
  padding: 28px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
}

.group-tag {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
  margin-bottom: 12px;
}

.group-card h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.group-card > p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.requirements h4 {
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 8px;
}

.requirements ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.requirements li {
  font-size: 13px;
  color: var(--text);
  padding: 4px 0;
  padding-left: 16px;
  position: relative;
}

.requirements li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--primary);
}

.process-section {
  padding: 0 32px 80px;
}

.process-section h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 32px;
  text-align: center;
}

.process-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 600px;
  margin: 0 auto;
}

.step-item {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-size: 16px;
  font-weight: 700;
  color: #04101f;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.step-content p {
  color: var(--muted);
  font-size: 14px;
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
  font-size: 32px;
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
</style>
