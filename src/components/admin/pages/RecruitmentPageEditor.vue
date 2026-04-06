<template>
  <div class="recruitment-editor">
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

    <!-- 小组招募 -->
    <div class="form-section">
      <h3>小组招募</h3>
      <div class="groups-list">
        <div v-for="(group, index) in content.groups" :key="index" class="group-card">
          <div class="card-header">
            <span>{{ group.name || `小组 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeGroup(index)">×</button>
          </div>
          
          <div class="form-row">
            <input v-model="group.name" placeholder="名称" @input="emitUpdate" />
            <input v-model="group.tag" placeholder="标签" @input="emitUpdate" />
          </div>
          
          <textarea v-model="group.description" placeholder="描述" rows="2" @input="emitUpdate"></textarea>
          
          <div class="sub-field">
            <label>要求（逗号分隔）</label>
            <input 
              :value="group.requirements?.join(', ')" 
              @input="updateRequirements(index, $event.target.value)"
              placeholder="编程基础, 学习能力强"
            />
          </div>
        </div>
      </div>
      <button class="add-btn" @click="addGroup">+ 添加小组</button>
    </div>

    <!-- 招募流程 -->
    <div class="form-section">
      <h3>招募流程</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sectionTitles.process" type="text" @input="emitUpdate" />
      </div>
      <div class="process-list">
        <div v-for="(step, index) in content.process" :key="index" class="process-item">
          <span class="step-number">{{ index + 1 }}</span>
          <input v-model="step.step" placeholder="步骤名称" @input="emitUpdate" />
          <input v-model="step.description" placeholder="步骤描述" class="flex-1" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeProcess(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addProcess">+ 添加步骤</button>
    </div>

    <!-- CTA 区域 -->
    <div class="form-section">
      <h3>CTA 区域</h3>
      <div class="form-group">
        <label>标题</label>
        <input v-model="content.cta.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>按钮文字</label>
          <input v-model="content.cta.buttonText" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>按钮链接</label>
          <input v-model="content.cta.buttonLink" type="text" @input="emitUpdate" />
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
  hero: { eyebrow: '', title: '', subtitle: '' },
  groups: [],
  process: [],
  cta: { title: '', buttonText: '', buttonLink: '' },
  sectionTitles: { process: '' }
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

function addGroup() {
  content.groups.push({ name: '', tag: '', description: '', requirements: [] })
  emitUpdate()
}

function removeGroup(index) {
  content.groups.splice(index, 1)
  emitUpdate()
}

function updateRequirements(index, value) {
  content.groups[index].requirements = value.split(',').map(s => s.trim()).filter(Boolean)
  emitUpdate()
}

function addProcess() {
  content.process.push({ step: '', description: '' })
  emitUpdate()
}

function removeProcess(index) {
  content.process.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.recruitment-editor {
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 12px;
}

.groups-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.group-card {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.group-card input,
.group-card textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.group-card input:focus,
.group-card textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.sub-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-field label {
  font-size: 12px;
  color: var(--muted);
}

.process-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.process-item {
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

.process-item input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.process-item input:first-of-type {
  width: 140px;
}

.flex-1 {
  flex: 1;
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
