<template>
  <div class="members-editor">
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

    <!-- 统计数据 -->
    <div class="form-section">
      <h3>统计数据</h3>
      <div class="items-list horizontal">
        <div v-for="(stat, index) in content.stats" :key="index" class="stat-item">
          <input v-model="stat.value" placeholder="数值" class="stat-value" @input="emitUpdate" />
          <input v-model="stat.label" placeholder="标签" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeStat(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addStat">+ 添加统计</button>
    </div>

    <!-- 成员列表 -->
    <div class="form-section">
      <h3>成员列表</h3>
      <div class="members-grid">
        <div v-for="(member, index) in content.members" :key="index" class="member-card">
          <div class="card-header">
            <span>{{ member.name || `成员 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeMember(index)">×</button>
          </div>
          <div class="form-row">
            <input v-model="member.name" placeholder="姓名" @input="emitUpdate" />
            <input v-model="member.role" placeholder="职位" @input="emitUpdate" />
          </div>
          <div class="form-row">
            <input v-model="member.group" placeholder="小组" @input="emitUpdate" />
            <ImageUploadField
              v-model="member.avatar"
              label="成员头像"
              hint="支持上传或填写 URL"
              @update:model-value="emitUpdate"
            />
          </div>
          <textarea v-model="member.description" placeholder="简介" rows="2" @input="emitUpdate"></textarea>
          
          <div class="sub-field">
            <label>技能标签（逗号分隔）</label>
            <input 
              :value="member.skills?.join(', ')" 
              @input="updateSkills(index, $event.target.value)"
              placeholder="Vue, Python, 设计"
            />
          </div>
          
          <div class="sub-field">
            <label>链接</label>
            <div class="links-row">
              <input v-model="member.links.github" placeholder="GitHub" @input="emitUpdate" />
              <input v-model="member.links.portfolio" placeholder="作品集" @input="emitUpdate" />
            </div>
          </div>
        </div>
      </div>
      <button class="add-btn" @click="addMember">+ 添加成员</button>
    </div>

    <div class="form-section">
      <h3>底部 CTA</h3>
      <div class="form-group">
        <label>标题</label>
        <input v-model="content.joinCta.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>描述</label>
        <input v-model="content.joinCta.description" type="text" @input="emitUpdate" />
      </div>
      <div class="form-row">
        <input v-model="content.joinCta.primaryButton.text" placeholder="主按钮文字" @input="emitUpdate" />
        <input v-model="content.joinCta.primaryButton.link" placeholder="主按钮链接" @input="emitUpdate" />
      </div>
      <div class="form-row">
        <input v-model="content.joinCta.secondaryButton.text" placeholder="次按钮文字" @input="emitUpdate" />
        <input v-model="content.joinCta.secondaryButton.link" placeholder="次按钮链接" @input="emitUpdate" />
      </div>
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
  stats: [],
  members: [],
  joinCta: {
    title: '',
    description: '',
    primaryButton: { text: '', link: '' },
    secondaryButton: { text: '', link: '' }
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

function addStat() {
  content.stats.push({ value: '', label: '' })
  emitUpdate()
}

function removeStat(index) {
  content.stats.splice(index, 1)
  emitUpdate()
}

function addMember() {
  content.members.push({
    name: '',
    role: '',
    group: '',
    avatar: '',
    description: '',
    skills: [],
    links: { github: '', portfolio: '' }
  })
  emitUpdate()
}

function removeMember(index) {
  content.members.splice(index, 1)
  emitUpdate()
}

function updateSkills(index, value) {
  content.members[index].skills = value.split(',').map(s => s.trim()).filter(Boolean)
  emitUpdate()
}
</script>

<style scoped>
.members-editor {
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
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.form-group input,
.form-group textarea {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.items-list.horizontal {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
}

.stat-item input {
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.stat-value {
  width: 80px;
  font-weight: 600;
  color: var(--primary) !important;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.member-card {
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
  margin-bottom: 4px;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.form-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 10px;
}

.form-row > * {
  min-width: 0;
}

.member-card input,
.member-card textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.member-card input:focus,
.member-card textarea:focus {
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

.links-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
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

.remove-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 16px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.2);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  font-size: 14px;
}
</style>
