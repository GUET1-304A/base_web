<template>
  <div class="onboarding-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-group">
        <label>小标签</label>
        <input v-model="content.hero.eyebrow" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>主标题</label>
        <input v-model="content.hero.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
    </div>

    <!-- 入职流程 -->
    <div class="form-section">
      <h3>入职流程</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.stepsTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="steps-list">
        <div v-for="(step, index) in content.steps" :key="index" class="step-item">
          <span class="step-number">{{ index + 1 }}</span>
          <input v-model="step.title" placeholder="步骤标题" @input="emitUpdate" />
          <input v-model="step.description" placeholder="步骤描述" class="flex-1" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeStep(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addStep">+ 添加步骤</button>
    </div>

    <!-- 资源中心 -->
    <div class="form-section">
      <h3>资源中心</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.resourcesTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="resources-grid">
        <div v-for="(resource, index) in content.resources" :key="index" class="resource-card">
          <div class="card-header">
            <span>{{ resource.title || `资源 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeResource(index)">×</button>
          </div>
          <input v-model="resource.title" placeholder="资源名称" @input="emitUpdate" />
          <input v-model="resource.description" placeholder="描述" @input="emitUpdate" />
          <select v-model="resource.icon" @change="emitUpdate">
            <option value="book">📚 Book</option>
            <option value="palette">🎨 Palette</option>
            <option value="code">💻 Code</option>
            <option value="chat">💬 Chat</option>
          </select>
        </div>
      </div>
      <button class="add-btn" @click="addResource">+ 添加资源</button>
    </div>

    <!-- 导师团队 -->
    <div class="form-section">
      <h3>导师团队</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.mentorsTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="mentors-grid">
        <div v-for="(mentor, index) in content.mentors" :key="index" class="mentor-card">
          <div class="card-header">
            <span>{{ mentor.name || `导师 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeMentor(index)">×</button>
          </div>
          <ImageUploadField
            v-model="mentor.avatar"
            label="导师头像"
            hint="支持上传或填写 URL"
            @update:model-value="emitUpdate"
          />
          <input v-model="mentor.name" placeholder="姓名" @input="emitUpdate" />
          <input v-model="mentor.role" placeholder="方向" @input="emitUpdate" />
          <textarea v-model="mentor.description" placeholder="简介" rows="2" @input="emitUpdate"></textarea>
        </div>
      </div>
      <button class="add-btn" @click="addMentor">+ 添加导师</button>
    </div>

    <!-- FAQ -->
    <div class="form-section">
      <h3>常见问题</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.faqTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="faq-list">
        <div v-for="(faq, index) in content.faq" :key="index" class="faq-item">
          <div class="item-header">
            <span>问题 {{ index + 1 }}</span>
            <button class="remove-btn small" @click="removeFaq(index)">×</button>
          </div>
          <input v-model="faq.question" placeholder="问题" @input="emitUpdate" />
          <textarea v-model="faq.answer" placeholder="答案" rows="2" @input="emitUpdate"></textarea>
        </div>
      </div>
      <button class="add-btn" @click="addFaq">+ 添加问题</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '' },
  steps: [],
  resources: [],
  mentors: [],
  faq: [],
  sections: {
    stepsTitle: '',
    resourcesTitle: '',
    mentorsTitle: '',
    faqTitle: ''
  }
}

const content = reactive({ ...defaultContent })

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
})

watch(() => props.modelValue, (newVal) => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...newVal })))
}, { deep: true })

function emitUpdate() {
  emit('update:modelValue', JSON.parse(JSON.stringify(content)))
}

function addStep() {
  content.steps.push({ title: '', description: '' })
  emitUpdate()
}

function removeStep(index) {
  content.steps.splice(index, 1)
  emitUpdate()
}

function addResource() {
  content.resources.push({ title: '', description: '', icon: 'book' })
  emitUpdate()
}

function removeResource(index) {
  content.resources.splice(index, 1)
  emitUpdate()
}

function addMentor() {
  content.mentors.push({ name: '', role: '', description: '', avatar: '' })
  emitUpdate()
}

function removeMentor(index) {
  content.mentors.splice(index, 1)
  emitUpdate()
}

function addFaq() {
  content.faq.push({ question: '', answer: '' })
  emitUpdate()
}

function removeFaq(index) {
  content.faq.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.onboarding-editor {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section h3::before {
  content: '';
  width: 4px;
  height: 16px;
  background: var(--primary);
  border-radius: 2px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
  font-size: 14px;
  font-weight: 700;
  color: #04101f;
  flex-shrink: 0;
}

.step-item input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.step-item input:first-of-type {
  width: 150px;
}

.flex-1 {
  flex: 1;
}

.resources-grid, .mentors-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.resource-card, .mentor-card {
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 13px;
  font-weight: 500;
  color: var(--primary);
}

.resource-card input,
.resource-card select,
.mentor-card input,
.mentor-card textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.resource-card input:focus,
.mentor-card input:focus,
.mentor-card textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.faq-item {
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-header span {
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
}

.faq-item input,
.faq-item textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.faq-item input:focus,
.faq-item textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.add-btn {
  padding: 10px 20px;
  border: 1px dashed var(--panel-border);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn.small:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
