<template>
  <div class="join-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-group">
        <label>主标题</label>
        <input v-model="content.hero.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
    </div>

    <!-- 加入优势 -->
    <div class="form-section">
      <h3>加入优势</h3>
      <div class="benefits-list">
        <div v-for="(benefit, index) in content.benefits" :key="index" class="benefit-item">
          <input v-model="benefit.title" placeholder="标题" @input="emitUpdate" />
          <input v-model="benefit.description" placeholder="描述" class="flex-1" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeBenefit(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addBenefit">+ 添加优势</button>
    </div>

    <!-- 小组选择 -->
    <div class="form-section">
      <h3>小组选择</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.groupsTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="groups-grid">
        <div v-for="(group, index) in content.form?.groups || []" :key="index" class="group-item">
          <div class="item-header">
            <span>{{ group.name || `小组 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeGroup(index)">×</button>
          </div>
          <input v-model="group.id" placeholder="ID (如: liuguang)" @input="emitUpdate" />
          <input v-model="group.name" placeholder="名称" @input="emitUpdate" />
          <input v-model="group.tag" placeholder="标签" @input="emitUpdate" />
        </div>
      </div>
      <button class="add-btn" @click="addGroup">+ 添加小组</button>
    </div>

    <div class="form-section">
      <h3>报名表单说明</h3>
      <div class="form-group">
        <label>GitHub 默认值</label>
        <input v-model="content.form.defaultGithubUrl" type="text" @input="emitUpdate" />
      </div>
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

    <div class="form-section">
      <h3>底部 CTA</h3>
      <div class="form-group">
        <label>标题</label>
        <input v-model="content.applyCta.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>描述</label>
        <input v-model="content.applyCta.description" type="text" @input="emitUpdate" />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>按钮文字</label>
          <input v-model="content.applyCta.buttonText" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>按钮链接</label>
          <input v-model="content.applyCta.link" type="text" @input="emitUpdate" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const defaultContent = {
  hero: { title: '', subtitle: '' },
  benefits: [],
  form: { groups: [], defaultGithubUrl: '' },
  faq: [],
  sections: { groupsTitle: '', faqTitle: '' },
  applyCta: { title: '', description: '', buttonText: '', link: '' }
}

const content = reactive({ ...defaultContent })

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
  if (!content.form) content.form = { groups: [], defaultGithubUrl: '' }
  if (!content.form.groups) content.form.groups = []
  if (!content.sections) content.sections = { groupsTitle: '', faqTitle: '' }
  if (!content.applyCta) content.applyCta = { title: '', description: '', buttonText: '', link: '' }
})

watch(() => props.modelValue, (newVal) => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...newVal })))
}, { deep: true })

function emitUpdate() {
  emit('update:modelValue', JSON.parse(JSON.stringify(content)))
}

function addBenefit() {
  content.benefits.push({ title: '', description: '' })
  emitUpdate()
}

function removeBenefit(index) {
  content.benefits.splice(index, 1)
  emitUpdate()
}

function addGroup() {
  if (!content.form) content.form = { groups: [] }
  content.form.groups.push({ id: '', name: '', tag: '' })
  emitUpdate()
}

function removeGroup(index) {
  content.form.groups.splice(index, 1)
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
.join-editor {
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

.benefits-list, .faq-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.benefit-item {
  display: flex;
  gap: 12px;
  align-items: center;
}

.benefit-item input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.benefit-item input:first-child {
  width: 150px;
}

.flex-1 {
  flex: 1;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.group-item, .faq-item {
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
  margin-bottom: 4px;
}

.item-header span {
  font-size: 13px;
  font-weight: 500;
  color: var(--primary);
}

.group-item input,
.faq-item input,
.faq-item textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.group-item input:focus,
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
