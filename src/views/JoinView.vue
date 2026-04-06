<template>
  <div class="join-page">
    <Navbar />
    
    <main class="join-main">
      <section class="join-hero">
        <h1>{{ pageData.hero?.title || '加入星雨作坊' }}</h1>
        <p>{{ pageData.hero?.subtitle || '与志同道合的伙伴一起，把想法变成现实。' }}</p>
      </section>

      <section class="benefits-section">
        <div class="benefits-grid">
          <div 
            v-for="(benefit, index) in (pageData.benefits || defaultBenefits)" 
            :key="index"
            class="benefit-card"
          >
            <h3>{{ benefit.title }}</h3>
            <p>{{ benefit.description }}</p>
          </div>
        </div>
      </section>

      <section class="groups-section">
        <h2>{{ pageData.sections?.groupsTitle || '选择你的方向' }}</h2>
        <div class="groups-grid">
          <div 
            v-for="group in (pageData.form?.groups || defaultGroups)" 
            :key="group.id"
            :class="['group-card', { selected: selectedGroup === group.id }]"
            @click="selectedGroup = group.id"
          >
            <span class="group-tag">{{ group.tag }}</span>
            <h3>{{ group.name }}</h3>
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

      <section class="apply-section">
        <div class="apply-card">
          <h2>{{ pageData.applyCta?.title || '准备好了吗？' }}</h2>
          <p>{{ pageData.applyCta?.description || '填写申请表，开启你的星雨之旅' }}</p>

          <form class="apply-form" @submit.prevent="submitApplication">
            <div class="form-grid">
              <input v-model.trim="applicationForm.name" type="text" placeholder="姓名" required />
              <input v-model.trim="applicationForm.student_id" type="text" placeholder="学号" required />
            </div>

            <div class="form-grid">
              <input v-model.trim="applicationForm.grade_major" type="text" placeholder="年级 / 专业" required />
              <input v-model.trim="applicationForm.phone" type="tel" placeholder="手机号" required />
            </div>

            <div class="form-grid">
              <input v-model.trim="applicationForm.email" type="email" placeholder="邮箱" required />
              <select v-model="applicationForm.group_id" required>
                <option value="">请选择报名方向</option>
                <option
                  v-for="group in (pageData.form?.groups || defaultGroups)"
                  :key="group.id"
                  :value="group.id"
                >
                  {{ group.name }} / {{ group.tag }}
                </option>
              </select>
            </div>

            <div class="form-grid">
              <input v-model.trim="applicationForm.github_url" type="url" placeholder="GitHub 链接（选填）" />
              <input v-model.trim="applicationForm.portfolio_url" type="url" placeholder="作品集 / 个人主页（选填）" />
            </div>

            <textarea
              v-model.trim="applicationForm.experience"
              rows="4"
              placeholder="相关经历（如项目、比赛、社团经历，可选）"
            ></textarea>

            <textarea
              v-model.trim="applicationForm.motivation"
              rows="5"
              placeholder="报名说明：请介绍你为什么想加入、想做什么、能投入多少时间"
              required
            ></textarea>

            <div v-if="submitMessage" :class="['submit-message', submitMessageType]">
              {{ submitMessage }}
            </div>

            <button class="apply-btn" type="submit" :disabled="submitting">
              {{ submitting ? '提交中...' : (pageData.applyCta?.buttonText || '提交申请') }}
            </button>
          </form>
        </div>
      </section>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { DEFAULT_APPLICATION_GITHUB_URL } from '../constants/externalLinks.js'

const pageData = ref({})
const selectedGroup = ref(null)
const submitting = ref(false)
const submitMessage = ref('')
const submitMessageType = ref('success')
const applicationForm = ref({
  name: '',
  student_id: '',
  grade_major: '',
  phone: '',
  email: '',
  group_id: '',
  github_url: DEFAULT_APPLICATION_GITHUB_URL,
  portfolio_url: '',
  experience: '',
  motivation: ''
})

const defaultBenefits = [
  { title: '真实项目经验', description: '参与从 0 到 1 的完整产品开发流程' },
  { title: '跨领域学习', description: '接触产品、设计、技术、运营各个方向' },
  { title: '开源贡献', description: '为开源社区贡献代码，积累 GitHub 履历' }
]

const defaultGroups = [
  { id: 'liuguang', name: '流光组', tag: '产品策划' },
  { id: 'xinghui', name: '星绘组', tag: '视觉设计' },
  { id: 'zhuyun', name: '逐云组', tag: '技术开发' },
  { id: 'huisheng', name: '回声组', tag: '内容传播' }
]

const defaultFaq = [
  { question: '需要什么基础才能加入？', answer: '我们欢迎所有热爱创造的同学，没有硬性技能要求。' },
  { question: '每周需要投入多少时间？', answer: '根据项目阶段不同，一般每周 4-8 小时。' },
  { question: '如何选择加入哪个小组？', answer: '可以根据自己的兴趣和特长选择主要方向。' }
]

watch(selectedGroup, (value) => {
  applicationForm.value.group_id = value || ''
})

watch(() => applicationForm.value.group_id, (value) => {
  selectedGroup.value = value || null
})

watch(() => pageData.value.form?.defaultGithubUrl, (value) => {
  if (
    !applicationForm.value.github_url ||
    applicationForm.value.github_url === DEFAULT_APPLICATION_GITHUB_URL
  ) {
    applicationForm.value.github_url = value || DEFAULT_APPLICATION_GITHUB_URL
  }
})

function resetApplicationForm() {
  applicationForm.value = {
    name: '',
    student_id: '',
    grade_major: '',
    phone: '',
    email: '',
    group_id: selectedGroup.value || '',
    github_url: pageData.value.form?.defaultGithubUrl || DEFAULT_APPLICATION_GITHUB_URL,
    portfolio_url: '',
    experience: '',
    motivation: ''
  }
}

async function submitApplication() {
  if (submitting.value) return

  const selectedGroupData = (pageData.value.form?.groups || defaultGroups).find(
    group => group.id === applicationForm.value.group_id
  )

  if (!selectedGroupData) {
    submitMessage.value = '请先选择报名方向'
    submitMessageType.value = 'error'
    return
  }

  submitting.value = true
  submitMessage.value = ''

  try {
    const result = await api.submitApplication({
      ...applicationForm.value,
      github_url:
        applicationForm.value.github_url === DEFAULT_APPLICATION_GITHUB_URL
          ? ''
          : applicationForm.value.github_url,
      group_name: selectedGroupData.name
    })

    submitMessage.value = result.message || '报名信息已提交'
    submitMessageType.value = result.warning ? 'warning' : 'success'
    resetApplicationForm()
  } catch (error) {
    submitMessage.value = error.message || '报名提交失败，请稍后重试'
    submitMessageType.value = 'error'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const data = await api.getPage('join')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load join page:', error)
  }
})
</script>

<style scoped>
.join-page { background: var(--bg); min-height: 100vh; }
.join-main { padding-top: 120px; max-width: 900px; margin: 0 auto; }

.join-hero {
  text-align: center;
  padding: 0 32px 80px;
}

.join-hero h1 {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.join-hero p {
  color: var(--muted);
  font-size: 18px;
}

.benefits-section { padding: 0 32px 80px; }

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.benefit-card {
  padding: 28px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
}

.benefit-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.benefit-card p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

.groups-section {
  padding: 0 32px 80px;
}

.groups-section h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
  text-align: center;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.group-card {
  padding: 24px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.group-card:hover { border-color: var(--primary); }
.group-card.selected { border-color: var(--primary); background: rgba(121, 168, 255, 0.1); }

.group-tag {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
  margin-bottom: 8px;
}

.group-card h3 {
  font-size: 18px;
  font-weight: 700;
}

.faq-section { padding: 0 32px 80px; }

.faq-section h2 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
  text-align: center;
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
  line-height: 1.6;
}

.apply-section { padding: 0 32px 120px; }

.apply-card {
  text-align: center;
  padding: 60px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
}

.apply-card h2 {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 12px;
}

.apply-card p {
  color: var(--muted);
  font-size: 16px;
  margin-bottom: 28px;
}

.apply-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.apply-form input,
.apply-form select,
.apply-form textarea {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.28);
  color: var(--text);
  font-size: 14px;
  box-sizing: border-box;
}

.apply-form input:focus,
.apply-form select:focus,
.apply-form textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.submit-message {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
}

.submit-message.success {
  background: rgba(70, 190, 120, 0.15);
  border: 1px solid rgba(70, 190, 120, 0.3);
  color: #8df2b2;
}

.submit-message.warning {
  background: rgba(255, 180, 50, 0.15);
  border: 1px solid rgba(255, 180, 50, 0.3);
  color: #ffcf70;
}

.submit-message.error {
  background: rgba(255, 100, 100, 0.15);
  border: 1px solid rgba(255, 100, 100, 0.3);
  color: #ff8d8d;
}

.apply-btn {
  display: inline-block;
  padding: 14px 40px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 999px;
  color: #04101f;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.apply-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(121, 168, 255, 0.25);
}

@media (max-width: 640px) {
  .groups-grid { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
}
</style>
